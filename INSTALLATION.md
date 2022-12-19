# Installation

The simplist way to try molflow is to use [offical docker image](#option-2-from-docker) which shipps with molflow binary.

Or you could [install molflow via Python Package Index](#option-1-from-pypi).

For advanced users, you could [install molflow from source](#option-3-from-source).

After installation, don't forget to [have a quick try](#a-quick-try) to check if molflow is good to go.

## Environment

Python：3.8

pip: >= 19.3

OS: CentOS 7, Ubuntu 18.04

CPU/Memory: recommended minimum requirement is 8C16G.

## Option 1: from pypi

For users who want to try molflow, you can install [the current release](https://pypi.org/project/molflow/)
from [pypi](https://pypi.org/project/molflow/). Note that it requires python version == 3.8, you can create a virtual environment with conda if not satisfied.

```
conda create -n sf python=3.8
conda activate sf
```

After that, please use pip to install molflow.

```bash
pip install -U molflow
```

## Option 2: from docker

You can also use molflow Docker image to give molflow a quick try.

The latest version can be obtained from [molflow tags](https://hub.docker.com/r/molflow/molflow-anolis8/tags).

```
export version={molflow version}
```

for example

```bash
export version=0.7.11b0
```

then run the image.

```bash
docker run -it molflow/molflow-anolis8:${version}

```

## Option 3: from source

1. Download code and set up Python virtual environment.

```sh
git clone https://github.com/Scientific-Simulation-Studio/MolFlow.git
cd molflow

conda create -n molflow python=3.8
conda activate molflow
```

2. Install molflow

```sh

python setup.py bdist_wheel

pip install dist/*.whl
```

## A quick try

Try your first molflow program.

```python
>>> import molflow as sf
>>> sf.init(['alice', 'bob', 'carol'], num_cpus=8, log_to_driver=True)
>>> dev = sf.PYU('alice')
>>> import numpy as np
>>> data = dev(np.random.rand)(3, 4)
>>> data
<molflow.device.device.pyu.PYUObject object at 0x7fdec24a15b0>
```
