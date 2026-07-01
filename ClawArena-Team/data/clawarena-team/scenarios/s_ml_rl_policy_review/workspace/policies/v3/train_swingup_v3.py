"""
PPO Curriculum Learning — ROTPEN Full Swing-up (alpha=pi → 0)

改进：
  - 自适应终止：到达顶端后离开才终止（防止转圈同时允许 swing-up 摆动）
  - 强化 near_top 奖励，增大 alive_bonus 在顶端附近
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import torch
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, BaseCallback

from common.rotpen_dynamics import rk4_step, wrap_alpha, VM_MAX

os.makedirs("models", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

PHASES = [
    {"name": "phase0_balance",   "al_range": np.radians(30),  "steps": 150_000},
    {"name": "phase1_medium",    "al_range": np.radians(90),  "steps": 150_000},
    {"name": "phase2_large",     "al_range": np.radians(150), "steps": 200_000},
    {"name": "phase3_fullswing", "al_range": np.radians(178), "steps": 500_000},
]

DEVICE = "cpu"
N_ENVS = 16


class CurriculumEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, al_range=np.radians(30), dt=0.005, max_steps=2000):
        super().__init__()
        self.al_range  = al_range
        self.dt        = dt
        self.max_steps = max_steps
        self.observation_space = spaces.Box(
            low=-np.ones(6, dtype=np.float32),
            high=np.ones(6, dtype=np.float32),
        )
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )
        self._state = None; self._step = 0
        self._was_upright = False   # 是否曾经到达顶端附近

    @property
    def state(self):
        return self._state.copy()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        rng = self.np_random
        al0 = rng.uniform(-self.al_range, self.al_range)
        self._state = np.array([
            rng.uniform(-0.05, 0.05), 0.0, al0, 0.0
        ], dtype=np.float64)
        self._step = 0
        self._was_upright = False
        return self._obs(), {}

    def step(self, action):
        Vm = float(action[0]) * VM_MAX
        self._state    = rk4_step(self._state, Vm, self.dt)
        self._state[0] = wrap_alpha(self._state[0])
        self._state[2] = wrap_alpha(self._state[2])
        self._state[1] = np.clip(self._state[1], -50., 50.)
        self._state[3] = np.clip(self._state[3], -50., 50.)
        self._step += 1

        th, th_d, al, al_d = self._state
        near_top = abs(al) < 0.4   # ~23°

        # 更新"曾经到达顶端"标志
        if near_top:
            self._was_upright = True

        # ── Reward ───────────────────────────────────────────
        upright   = (np.cos(al) + 1.0) ** 2
        alive_bon = 4.0 * float(near_top) * max(0., 1. - 0.05*al_d**2)
        u_pen     = 0.01 * (Vm / VM_MAX)**2
        th_pen    = 0.01 * np.sin(th)**2
        reward    = upright + alive_bon - u_pen - th_pen

        # ── 自适应终止 ───────────────────────────────────────
        # 仅当曾经到达顶端后再离开才终止（防转圈+允许摆起）
        fell_after_upright = self._was_upright and abs(al) > 0.5
        terminated = bool(fell_after_upright)
        truncated  = self._step >= self.max_steps
        return self._obs(), reward, terminated, truncated, {"al": al}

    def _obs(self):
        th, th_d, al, al_d = self._state
        return np.array([
            np.cos(th), np.sin(th), np.clip(th_d/15., -1, 1),
            np.cos(al), np.sin(al), np.clip(al_d/20., -1, 1),
        ], dtype=np.float32)


class RewardLog(BaseCallback):
    def __init__(self):
        super().__init__()
        self.ep_rewards = []

    def _on_step(self):
        for info in self.locals.get("infos", []):
            if "episode" in info:
                self.ep_rewards.append(info["episode"]["r"])
        return True


def make_env_fn(al_range):
    def _make():
        return CurriculumEnv(al_range=al_range, dt=0.005, max_steps=2000)
    return _make


if __name__ == "__main__":
    all_rewards = []
    model = None

    for ph in PHASES:
        name     = ph["name"]
        al_range = ph["al_range"]
        steps    = ph["steps"]
        print(f"\n{'='*50}")
        print(f"Phase: {name}  al_range={np.degrees(al_range):.0f}°  steps={steps}")
        print('='*50)

        env      = make_vec_env(make_env_fn(al_range), n_envs=N_ENVS)
        eval_env = make_vec_env(make_env_fn(al_range), n_envs=4)
        eval_cb  = EvalCallback(
            eval_env,
            best_model_save_path=f"models/{name}",
            log_path=f"outputs/logs/{name}",
            eval_freq=20_000,
            n_eval_episodes=20,
            deterministic=True,
            verbose=0,
        )
        rew_cb = RewardLog()

        if model is None:
            model = PPO(
                "MlpPolicy", env, device=DEVICE, verbose=1,
                learning_rate=3e-4, n_steps=2048,
                batch_size=256, n_epochs=10,
                gamma=0.99, gae_lambda=0.95,
                clip_range=0.2, ent_coef=0.005,
                policy_kwargs=dict(
                    net_arch=dict(pi=[128, 128], vf=[128, 128]),
                    activation_fn=torch.nn.Tanh,
                ),
                tensorboard_log="outputs/logs/tb/",
            )
        else:
            model.set_env(env)
            model.learning_rate = 1e-4

        model.learn(
            total_timesteps=steps,
            callback=[eval_cb, rew_cb],
            progress_bar=True,
            reset_num_timesteps=True,
        )
        model.save(f"models/{name}_final")
        all_rewards.extend(rew_cb.ep_rewards)
        print(f"Phase {name} done.  mean_rew={np.mean(rew_cb.ep_rewards[-200:]):.1f}")

    model.save("models/ppo_curriculum_final")
    np.save("outputs/logs/ep_rewards_curriculum.npy", np.array(all_rewards))
    print("\nAll phases complete.")
