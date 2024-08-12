[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/pyreprism)](https://pepy.tech/project/pyreprism)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=license)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=license)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=security)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=security)
[![Documentation Status](https://readthedocs.org/projects/pyreprism/badge/?version=latest)](https://pyreprism.readthedocs.io/en/latest/?badge=latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PyReprism)
![CI](https://github.com/unlv-evol/PyReprism/actions/workflows/ci.yml/badge.svg)
![Publish](https://github.com/unlv-evol/PyReprism/actions/workflows/publish.yml/badge.svg)
[![codecov](https://codecov.io/gh/unlv-evol/PyReprism/graph/badge.svg?token=J2JV31837H)](https://codecov.io/gh/unlv-evol/PyReprism)
![PyPI - Version](https://img.shields.io/pypi/v/pyreprism)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unlv-evol/pyreprism/main)
[![SWH](https://archive.softwareheritage.org/badge/origin/https://pypi.org/project/PyReprism//)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://pypi.org/project/PyReprism/)

# PyReprism

PyReprism is a Python framework that helps researchers and developers the task of source code preprocessing. With PyReprism, you can easily match, extract, count, and remove comments, whitespaces, operators, numbers and other language specific constructs from over **150 programming languages and file extensions**.

## Install
```shell
pip install PyReprism
```
## Quick Usage
Use case 1: Removing comments 
```python

from PyReprism.languages import Python
# from PyReprism.languages import Java

source = """
# single line comment
x = 5 + 6
'''
multiline
comment
'''
print(x)
"""

source = Python.remove_comments(source)

# expected output

x = 5 + 6


print(x)

```

Use case 2: Removing whitespaces 
```python
from PyReprism.utils.normalizer import Normalizer
source = """

x = 5 + 6


print(x)

"""


source = Normalizer.remove_whitespaces(source)

# expected output
x=5+6
print(x)
```

Read the [docs](https://pyreprism.readthedocs.io) for more usage examples. 

NB: The beta versions of PyReprism is still unstable, but we are working 24/7 to ensure the tool is usable.

## How to Contribute
We invite you to help us build this tool and make it more extensive. Contribution is open to OSS community.

```shell
$ git clone https://github.com/unlv-evol/PyReprism.git
$ cd PyReprism
```
**(Optional)** It is suggested to make use of virtualenv. Therefore, before installing the requirements run:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

Then, install the requirements:

```shell
$ pip install -r requirements.txt
```
For more information on how to contribute, read our [contributing guidelines](CONTRIBUTING.md).

## Issues
If you experience any issue, feel free to report it.
