from .env import *

import gym
from gym.envs.registration import register

env_dict = gym.envs.registration.registry.env_specs.copy()

for env in env_dict:
    if 'SimpleMemoryTestingEnv' in env:
        del gym.envs.registration.registry.env_specs[env]

register(
    id='SimpleMemoryTestingEnv-v0',
    entry_point='simple_memory_testing_env.env:generate_env'
)

register(
    id='SimpleMemoryTestingEnv-2Colors-v0',
    entry_point='simple_memory_testing_env.env:generate_2colors_env'
)

register(
    id='SimpleMemoryTestingEnv-Easy-v0',
    entry_point='simple_memory_testing_env.env:generate_easy_env'
)

register(
    id='SimpleMemoryTestingEnv-Easy-2Colors-v0',
    entry_point='simple_memory_testing_env.env:generate_easy_2colors_env'
)
