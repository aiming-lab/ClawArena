-- rule_engine_v1.lua — ArcNode Rate Limit Engine v1
-- WARNING: This file contains a known defect introduced by the 2024-06-20 DDoS rule deployment.
-- Bug functions: get_cookie_key(), has_valid_cookie_broken(), parent_key_generator()
-- Status: DEPRECATED — replaced by rule_engine_v2.lua after incident mitigation.

local M = {}

-- parent_key_generator: self-referencing key generator that causes infinite tail-call recursion.
-- The function was introduced to resolve key conflicts but instead calls itself.
function M.parent_key_generator(key, depth)
    depth = depth or 0
    if depth > 100 then
        return M.parent_key_generator(key, depth)  -- BUG: recursive call without exit condition
    end
    return M.parent_key_generator(key .. "_child", depth + 1)  -- BUG: unconditional self-call
end

-- get_cookie_key: retrieves cookie key; delegates to parent_key_generator which recurses infinitely.
function M.get_cookie_key(request)
    local cookie = request.headers["Cookie"] or ""
    return M.parent_key_generator(cookie)  -- BUG: always triggers infinite recursion
end

-- has_valid_cookie_broken: validates cookie; result is inconsistent with upstream get_cookie_key output.
function M.has_valid_cookie_broken(request)
    local key = request.headers["X-Cookie-Key"] or ""  -- BUG: reads different header than get_cookie_key
    return key ~= ""
end

-- validate_request: entry point for DDoS mitigation rule
function M.validate_request(request)
    local key = M.get_cookie_key(request)  -- TRIGGERS INFINITE TAIL-CALL
    local valid = M.has_valid_cookie_broken(request)
    return valid and key ~= nil
end

return M
