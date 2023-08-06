# SimpleMemoryTestingEnv

This is a simple OpenAI Gym-compatible environment to test RL agent's memory.

## Usage

`gym` must be installed. Environments can be created as follows:

```python
>>> import gym
>>> import simple_memory_testing_env
>>> env = gym.make("SimpleMemoryTestingEnv-v0")
```

+ default environment (partial observability + memory-requiring T-maze with 4 different colors) : `"SimpleMemoryTestingEnv-v0"` (with only 2 colors: `"SimpleMemoryTestingEnv-2Colors-v0"`)

![default_env](https://www.github.com/Near32/SimpleMemoryTestingEnv/raw/master/resources/normal.gif)

+ easy environment (partial observability maze with 4 different colors) : `"SimpleMemoryTestingEnv-Easy-v0"` (with only 2 colors: `"SimpleMemoryTestingEnv-Easy-2Colors-v0"`)

![easy_env](https://www.github.com/Near32/SimpleMemoryTestingEnv/raw/master/resources/easy.gif)


## Installation

### Installing via pip

This package is available in PyPi as `simple_memory_testing_env`

```bash
pip install simple_memory_testing_env
```

### Installing via cloning this repository

```bash
git clone https://www.github.com/Near32/SimpleMemoryTestingEnv
cd SimpleMemoryTestingEnv
pip install -e .
```