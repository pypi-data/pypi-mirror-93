from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='simple_memory_testing_env',
    version='0.0.1',
    description='OpenAI Gym-compatible implementation of a simple memory-testing environment.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Near32/SimpleMemoryTestingEnv',
    classifiers=[
      "Intended Audience :: Developers",
      "Topic :: Scientific/Engineering :: Artificial Intelligence ",
      "Programming Language :: Python :: 3",
    ],

    packages=find_packages(),
    zip_safe=False,

    install_requires=[
      'gym',
      'gym-minigrid',
    ],

    python_requires=">=3.6",
)
