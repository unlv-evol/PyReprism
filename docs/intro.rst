.. _intro_toplevel:

==================
Overview / Install
==================

PyReprism is a Python framework that helps researchers and developers the task of source code preprocessing. With PyReprism, you can easily match, extract, count, and remove comments, whitespaces, operators, numbers and other language specific constructs from over 150 programming languages and file extensions.


Requirements
============

* `Python`_ 3.6 or newer
* `Git`_

.. _Python: https://www.python.org
.. _Git: https://git-scm.com/

Installing PyReprism
====================

Installing PyReprism is easily done using `pip`_. Assuming it is installed, just run the following from the command-line:

.. _pip: https://pip.pypa.io/en/latest/installing.html

.. sourcecode:: none

    $ pip install PyReprism

Source Code
===========

PyReprism's git repo is available on GitHub, which can be browsed at:

 * https://github.com/unlv-evol/PyReprism.git

and cloned using::

    $ git clone https://github.com/unlv-evol/PyReprism.git
    $ cd PyReprism

Optionally (but suggested), make use of virtual environment. Therefore, before installing the requirements run::
    
    $ python3 -m venv venv
    $ source venv/bin/activate

Install the requirements::
    
    $ pip install -r requirements.txt

and run the tests using pytest::

    $ pytest
