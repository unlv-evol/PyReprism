[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![PyPI - Downloads](https://img.shields.io/pypi/dw/PyReprism)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=license)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=license)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=security)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=security)
[![Documentation Status](https://readthedocs.org/projects/pyreprism/badge/?version=latest)](https://pyreprism.readthedocs.io/en/latest/?badge=latest)


# PyReprism

PyReprism is a suite of essential methods designed for common preprocessing tasks in code clone detection research.

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
```

Use case 2: Removing whitespaces 
```python
from PyReprism.utils.normalizer import Normalizer
source = """

x = 5 + 6


print(x)
"""

source = Normalizer.remove_whitespaces(source)
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
## Issues
If you experience any issue, feel free to report it here. We are developing the issue reporting guidelines which will be available soon.
