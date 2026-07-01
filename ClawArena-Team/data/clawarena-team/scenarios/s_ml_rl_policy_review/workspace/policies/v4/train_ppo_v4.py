"""
PPO 训练 ROTPEN 平衡控制，使用 GPU。
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import (
    EvalCallback, BaseCallback
)
from stable_baselines3.common.vec_env import VecNormalize

from src.envs.rotpen_env import RotPenEnv

# v4 修改：在 wrapper 里加一项 distance bonus
# 见 docs/v4_changelog.md（QA 标记为可能导致 swingup 失稳）

os.makedirs("models", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

DEVICE = "cpu"   # PPO MLP 在 CPU 更高效
print(f"Using device: {DEVICE}")


class RewardLogCallback(BaseCallback):
    """记录每 episode 的 reward 均值，供后续作图。"""
    def __init__(self):
        super().__init__()
        self.ep_rewards = []
        self._current_rewards = {}

    def _on_step(self):
        infos = self.locals.get("infos", [])
        for i, info in enumerate(infos):
            if "episode" in info:
                self.ep_rewards.append(info["episode"]["r"])
        return True


def make_env():
    return RotPenEnv(dt=0.005, max_steps=2000)


if __name__ == "__main__":
    n_envs = 16   # 并行环境数（GPU 时可多开）
    env = make_vec_env(make_env, n_envs=n_envs)

    eval_env = make_vec_env(make_env, n_envs=4)
    eval_cb = EvalCallback(
        eval_env,
        best_model_save_path="models/",
        log_path="outputs/logs/",
        eval_freq=20_000,
        n_eval_episodes=20,
        deterministic=True,
        verbose=0,
    )
    reward_cb = RewardLogCallback()

    model = PPO(
        "MlpPolicy",
        env,
        device=DEVICE,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=256,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.005,
        policy_kwargs=dict(
            net_arch=dict(pi=[128, 128], vf=[128, 128]),
            activation_fn=torch.nn.Tanh,
        ),
        tensorboard_log="outputs/logs/tb/",
    )

    print("Training PPO ...")
    model.learn(
        total_timesteps=1_000_000,
        callback=[eval_cb, reward_cb],
        progress_bar=True,
    )

    model.save("models/ppo_rotpen_final")
    np.save("outputs/logs/ep_rewards.npy", np.array(reward_cb.ep_rewards))
    print("Training done. Model saved.")
