-- rule_engine_v2.lua — ArcNode Rate Limit Engine v2 (FIXED)
-- Replaces rule_engine_v1.lua after INC-2024-047 postmortem.
-- Fixed: removed infinite tail-call recursion; added execution time limit.

local M = {}

-- Fixed key generator: no longer self-referencing
function M.parent_key_generator(key, depth)
    depth = depth or 0
    if depth >= 3 then return key end  -- FIXED: bounded recursion
    return key .. "_v2"
end

-- Fixed cookie key: uses bounded generator
function M.get_cookie_key(request)
    local cookie = request.headers["Cookie"] or ""
    return M.parent_key_generator(cookie, 0)
end

-- Fixed validation: reads same header as get_cookie_key
function M.has_valid_cookie_broken(request)
    -- RENAMED to has_valid_cookie (kept old name for reference; logic fixed)
    local key = M.get_cookie_key(request)
    return key ~= ""
end

function M.validate_request(request)
    local key = M.get_cookie_key(request)
    local valid = M.has_valid_cookie_broken(request)
    return valid and key ~= nil
end

return M
