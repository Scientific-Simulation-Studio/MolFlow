# Installation

The simplist way to try moleculeflow is to use [offical docker image](#option-2-from-docker) which shipps with moleculeflow binary.

Or you could [install moleculeflow via Python Package Index](#option-1-from-pypi).

For advanced users, you could [install moleculeflow from source](#option-3-from-source).

After installation, don't forget to [have a quick try](#a-quick-try) to check if moleculeflow is good to go.


## Environment
Python：3.8

pip: >= 19.3

OS: CentOS 7, Ubuntu 18.04

CPU/Memory: recommended minimum requirement is 8C16G.

## Option 1: from pypi
For users who want to try moleculeflow, you can install [the current release](https://pypi.org/project/moleculeflow/)
from [pypi](https://pypi.org/project/moleculeflow/). Note that it requires python version == 3.8, you can create a virtual environment with conda if not satisfied.

```
conda create -n sf python=3.8
conda activate sf
```

After that, please use pip to install moleculeflow.

```bash
pip install -U moleculeflow
```

## Option 2: from docker
You can also use moleculeflow Docker image to give moleculeflow a quick try.

The latest version can be obtained from [moleculeflow tags](https://hub.docker.com/r/moleculeflow/moleculeflow-anolis8/tags).

```
export version={moleculeflow version}
```

for example
```bash
export version=0.7.11b0
```

then run the image.
```bash
docker run -it moleculeflow/moleculeflow-anolis8:${version}

```

## Option 3: from source

1. Download code and set up Python virtual environment.

```sh
git clone https://github.com/moleculeflow/moleculeflow.git
cd moleculeflow

conda create -n moleculeflow python=3.8
conda activate moleculeflow
```

2. Install moleculeflow
```sh

python setup.py bdist_wheel

pip install dist/*.whl
```

## A quick try
Try your first moleculeflow program.

```python
>>> import moleculeflow as sf
>>> sf.init(['alice', 'bob', 'carol'], num_cpus=8, log_to_driver=True)
>>> dev = sf.PYU('alice')
>>> import numpy as np
>>> data = dev(np.random.rand)(3, 4)
>>> data
<moleculeflow.device.device.pyu.PYUObject object at 0x7fdec24a15b0>
```
