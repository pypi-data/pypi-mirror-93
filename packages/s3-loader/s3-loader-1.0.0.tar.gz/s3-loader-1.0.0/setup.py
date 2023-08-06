# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_loader']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.63,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['s3-uploader = s3_loader.main:app']}

setup_kwargs = {
    'name': 's3-loader',
    'version': '1.0.0',
    'description': 'wrapper script for uploading files and dirs to s3',
    'long_description': None,
    'author': 'phil-bell',
    'author_email': 'philhabell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.12,<4.0.0',
}


setup(**setup_kwargs)
