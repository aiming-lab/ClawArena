/**
 * MM-MetaClaw OpenClaw plugin vendored into ClawArena.
 */

import { emptyPluginConfigSchema } from "openclaw/plugin-sdk/core";

const GATEWAY = process.env.METACLAW_GATEWAY ?? "http://127.0.0.1:30100";
const MODEL_HINT = process.env.METACLAW_MODEL_HINT ?? "openclaw";

let enabledModulesPromise: Promise<Set<string>> | null = null;

function getEnabledModules(): Promise<Set<string>> {
  if (!enabledModulesPromise) {
    enabledModulesPromise = fetch(`${GATEWAY}/v1/health`, {
      signal: AbortSignal.timeout(1500),
    })
      .then((r) => r.json() as Promise<{ modules?: string[] }>)
      .then((d) => new Set(d.modules ?? []))
      .catch(() => new Set<string>());
  }
  return enabledModulesPromise;
}

const skillGenerationCache = new Map<string, number>();

const plugin = {
  id: "mm-metaclaw",
  name: "MM-MetaClaw",
  description: "MM-MetaClaw skill/memory injection and RL model hot-swap",
  configSchema: emptyPluginConfigSchema(),
  register(api) {
    api.on("before_model_resolve", async (event, ctx) => {
      const enabled = await getEnabledModules();
      if (!enabled.has("rl")) {
        return {};
      }

      const res = await post(`${GATEWAY}/v1/rl/resolve`, {
        session_id: ctx.sessionId ?? "default",
        messages: [{ role: "user", content: event.prompt }],
        model: MODEL_HINT,
        metadata: { agent_type: "openclaw" },
      });
      return {
        modelOverride: res.model ?? undefined,
        providerOverride: res.provider ?? undefined,
      };
    });

    api.on("before_prompt_build", async (event, ctx) => {
      const enabled = await getEnabledModules();
      const sessionId = ctx.sessionId ?? "default";
      const req = {
        session_id: sessionId,
        messages: coerceMessages(event.messages),
        model: MODEL_HINT,
        metadata: { agent_type: "openclaw" },
      };

      const tasks: Promise<Record<string, unknown>>[] = [];
      const order: string[] = [];
      for (const module of ["memory", "skill"] as const) {
        if (enabled.has(module)) {
          tasks.push(post(`${GATEWAY}/v1/${module}/inject`, req));
          order.push(module);
        }
      }

      const results = await Promise.all(tasks);
      const skillIdx = order.indexOf("skill");
      if (skillIdx !== -1) {
        const gen =
          (results[skillIdx].metadata as Record<string, unknown>)?.skill_generation ?? 0;
        skillGenerationCache.set(sessionId, Number(gen) || 0);
      }

      const parts = results
        .map((r) => r.additional_context as string | undefined)
        .filter(Boolean) as string[];

      return {
        prependContext: parts.join("\n\n"),
      };
    });

    api.on("agent_end", async (event, ctx) => {
      const enabled = await getEnabledModules();
      const sessionId = ctx.sessionId ?? "default";
      const skillGen = skillGenerationCache.get(sessionId) ?? 0;
      skillGenerationCache.delete(sessionId);

      const req = {
        session_id: sessionId,
        trajectory: coerceMessages(event.messages),
        metadata: {
          model: MODEL_HINT,
          success: event.success,
          duration_ms: event.durationMs ?? 0,
          agent_type: "openclaw",
          skill_generation: skillGen,
          turn_type: "main",
        },
      };

      if (enabled.has("skill")) {
        await post(`${GATEWAY}/v1/skill/collect`, req);
      }

      await Promise.allSettled([
        enabled.has("memory") ? post(`${GATEWAY}/v1/memory/collect`, req) : Promise.resolve(),
        enabled.has("rl") ? post(`${GATEWAY}/v1/rl/collect`, req) : Promise.resolve(),
      ]);
    });
  },
};

export default plugin;

async function post(url: string, body: unknown): Promise<Record<string, unknown>> {
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(5000),
    });
    if (!r.ok) {
      return {};
    }
    return r.json() as Promise<Record<string, unknown>>;
  } catch {
    return {};
  }
}

function coerceMessages(messages: unknown[]): Array<Record<string, unknown>> {
  return messages.filter((msg): msg is Record<string, unknown> => {
    return Boolean(msg) && typeof msg === "object" && !Array.isArray(msg);
  });
}
