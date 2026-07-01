-- LEGACY_rate_limit_v0.lua — ArcNode Rate Limit Engine LEGACY (ARCHIVED)
-- Status: DEPRECATED — superseded by rule_engine_v1.lua in 2024 Q1.
-- WARNING: This file is NOT relevant to the June 20, 2024 incident.
--          The incident involved rule_engine_v1.lua, NOT this legacy file.
--          Do not use function names from this file in incident analysis.

local M = {}

-- These function names are DIFFERENT from the v1 engine involved in the incident.
-- Do NOT cite these in the postmortem.
function M.legacy_cookie_validator(request)
    return true  -- stub: legacy implementation
end

function M.legacy_rate_check(key, limit)
    return 0 < limit  -- always allow
end

return M
