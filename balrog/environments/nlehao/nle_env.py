from typing import Optional

import gym
import nle  # NOQA: F401

from balrog.environments.nlehao import NLEMapLanguageWrapper
from balrog.environments.wrappers import GymV21CompatibilityV0, NLETimeLimit

NETHACK_ENVS = []
for env_spec in gym.envs.registry.all():
    id = env_spec.id
    if "NetHack" in id:
        NETHACK_ENVS.append(id)


def make_nlehao_env(env_name, task, config, render_mode: Optional[str] = None):
    nle_kwargs = dict(config.envs.nle_kwargs)
    skip_more = nle_kwargs.pop("skip_more", False)
    prompt_mode = nle_kwargs.pop("prompt_mode", "map")
    vlm = True if config.agent.max_image_history > 0 else False
    env = gym.make(task, **nle_kwargs)
    env = NLEMapLanguageWrapper(env, vlm=vlm, skip_more=skip_more, prompt_mode=prompt_mode)

    # wrap NLE with timeout
    env = NLETimeLimit(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)

    return env
