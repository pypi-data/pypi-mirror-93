# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confirm']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['confirm = confirm.__main__:main']}

setup_kwargs = {
    'name': 'cli-confirm',
    'version': '1.0.0',
    'description': 'CLI utility to confirm yes/no.',
    'long_description': 'cli-confirm\n===========\n\n[![Test](https://github.com/tueda/cli-confirm/workflows/CI/badge.svg?branch=master)](https://github.com/tueda/cli-confirm/actions?query=branch:master)\n[![PyPI version](https://badge.fury.io/py/cli-confirm.svg)](https://pypi.org/project/cli-confirm/)\n\nA CLI utility to confirm yes/no.\n\n\nInstallation\n------------\n\n```sh\npip install cli-confirm\n```\n\n\nExample\n-------\n\n```sh\nconfirm \'Are you sure?\'\n```\nwhich shows a prompt to ask yes/no:\n```\nAre you sure? [y/N]:\n```\nIf the user answers "yes", then it returns a zero exit status.\nIt returns a non-zero exit status otherwise.\n\n\nMotivation\n----------\n\nThis utility can be used in a combination with [taskipy](https://github.com/illBeRoy/taskipy) as follows:\n\n```toml\n[tool.taskipy.tasks]\ndeploy = "confirm \'Are you sure to deploy?\' && mkdocs gh-deploy"\n```\n\n\nLicense\n-------\n\n[MIT](https://github.com/tueda/cli-confirm/blob/master/LICENSE)\n',
    'author': 'Takahiro Ueda',
    'author_email': 'takahiro.ueda@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tueda/cli-confirm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
