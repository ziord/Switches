<!-- <div align="center">
<img alt="leap image" src="assets/switches_256x256.png"/>
</div> -->
<p align="center">
    <p align="center">
        <img alt="Switches image" src="assets/switches_256x256.png" >
    </p>
    <p align="center">
        <a href="https://www.python.org/">
            <img alt="built with python" src="https://img.shields.io/badge/built%20with-python-blue.svg?style=plastic" >
        </a>
        <a href="https://github.com/ziord/Switches/blob/master/LICENSE.txt">
            <img alt="Spy License" src="https://img.shields.io/github/license/ziord/Switches?style=plastic" >
        </a>
        <a href="https://www.python.org/downloads/">
            <img alt="python versions (3.6+)" src="https://img.shields.io/badge/python-3.6+-blue.svg?style=plastic">
        </a>
        <a href="https://github.com/ziord/Switches/issues" >
            <img alt="issues" src="https://img.shields.io/github/issues/ziord/Switches?style=plastic">
        </a>
        <a href="https://github.com/ziord/Switches/stargazers">
            <img alt="stars" src="https://img.shields.io/github/stars/ziord/Switches?style=plastic">
        </a>
        <a href="https://github.com/ziord/Switches/network/members">
            <img alt="forks" src="https://img.shields.io/github/forks/ziord/Switches?style=plastic">
        </a>
    </p>
</p>

<br />

## Table of Contents
- [ Overview ](#about)
- [Usage](#usage)
- [ Documentation](#docs)
- [Tests](#tests)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [License](#license)

\
\
<a name='about'></a>
# Switches

`if` statements in Python can become cluttered when there are too many conditions to check or match, and more often, there is need to make these multiple `if` constructs more readable, syntactically clearer or at the very least aesthetically pleasing :), thus arising the inspiration for Switches.

Switches is a package that helps support C-like switch statements (and more!) in Python.

\
\
<a name='usage'></a>
## Usage

Consider the following (overly simplified) code snippet:

```python
val = get_some_value()
if val == 10:
    do_stuff1()
elif val == 15:
    do_stuff2()
elif val == 20:
    do_stuff3()
elif val == 30:
    do_stuff4()
else:
    do_other_stuff()
```
Using Switches, we could rewrite this as:

```python
from switches.switch import switch

val = get_some_value()
with switch(val) as s:
    s.case(10, do_stuff1)
    s.case(15, do_stuff2)
    s.case(20, do_stuff3)
    s.case(30, do_stuff4)
    s.default(do_other_stuff)
```
When writing `if` conditional tests of equality, Switches can make things pretty easier.
In the snippet above, `break`s are automatically (implicitly) added to each `case` statement when `fallthrough` is set to `False`(`False` by default), unlike C-style switches.

For more information about `fallthrough` attribute and `break` statements see the [doc](https://github.com/ziord/Switches/blob/master/DOCUMENTATION).
\
\
<a name='docs'></a>
## Documentation
More information is contained in the documentation.
[Read the docs](https://github.com/ziord/Switches/blob/master/DOCUMENTATION).

\
<a name='tests'></a>
## Tests
See the [tests](https://github.com/ziord/Switches/blob/master/tests) folder for tests and other examples.

\
<a name='installation'></a>
## Installation
Clone this repo, and do:

`cd Switches` <br/> `python setup.py install`
\
<a name='dependencies'></a>
## Dependencies
Python 3.6+

\
<a name='license'></a>
## License
[MIT](https://github.com/ziord/Switches/blob/master/LICENSE)