[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![PyPI - Downloads](https://img.shields.io/pypi/dd/PyReprism)
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
# single line comment
x = 5 + 6
'''
multiline
comment
'''
print(x)
"""

source = Normalizer.remove_whitespaces(source)
```

Read the [docs]() for more usage examples. -- Coming soon!!

NB: The beta versions of PyReprism is still highly unstable, we are working 24/7 to ensure the tool is usable.

## How to Contribute
We invite you to help us build this tool and make it more extensive. Contribution is open to OSS community.

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
## Issues
If you experience any issue, feel free to report it here. We are developing the issue reporting guidelines which will be available soon.
