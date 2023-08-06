# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mail_alias_creator', 'mail_alias_creator.entry_processors']

package_data = \
{'': ['*']}

install_requires = \
['ldap3>=2.7,<3.0', 'pyyaml>=5.2,<6.0']

entry_points = \
{'console_scripts': ['mail_alias_creator = mail_alias_creator.main:main']}

setup_kwargs = {
    'name': 'mail-alias-creator',
    'version': '1.0.0',
    'description': 'Set of pyhton scripts to create our mail alias tables from alias definitions',
    'long_description': None,
    'author': 'Tim Neumann',
    'author_email': 'neumantm@fius.informatik.uni-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
