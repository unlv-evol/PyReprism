[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# PyReprism

PyReprism is a suite of essential methods designed for common preprocessing tasks in code clone detection research.

## Install
```shell
pip install PyReprism
```
## Quick Usage
```python

from PyReprism.languages import Python

source = """
# single line comment
x = 5 + 6
'''
multiline
comment
'''
print(x)
"""

source =''.join(Python.remove_comments(source))
```
Read the [docs]() for more usage examples. 

## How to Contribute

```shell
git clone https://github.com/unlv-evol/PyReprism.git
cd PyReprism
```
**(Optional)** It is suggested to make use of virtualenv. Therefore, before installing the requirements run:

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```
