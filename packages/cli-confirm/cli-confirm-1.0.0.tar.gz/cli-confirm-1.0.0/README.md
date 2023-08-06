cli-confirm
===========

[![Test](https://github.com/tueda/cli-confirm/workflows/CI/badge.svg?branch=master)](https://github.com/tueda/cli-confirm/actions?query=branch:master)
[![PyPI version](https://badge.fury.io/py/cli-confirm.svg)](https://pypi.org/project/cli-confirm/)

A CLI utility to confirm yes/no.


Installation
------------

```sh
pip install cli-confirm
```


Example
-------

```sh
confirm 'Are you sure?'
```
which shows a prompt to ask yes/no:
```
Are you sure? [y/N]:
```
If the user answers "yes", then it returns a zero exit status.
It returns a non-zero exit status otherwise.


Motivation
----------

This utility can be used in a combination with [taskipy](https://github.com/illBeRoy/taskipy) as follows:

```toml
[tool.taskipy.tasks]
deploy = "confirm 'Are you sure to deploy?' && mkdocs gh-deploy"
```


License
-------

[MIT](https://github.com/tueda/cli-confirm/blob/master/LICENSE)
