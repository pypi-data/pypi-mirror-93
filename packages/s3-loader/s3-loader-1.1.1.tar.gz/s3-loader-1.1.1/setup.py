# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_loader']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.63,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['s3-loader = s3_loader.main:app']}

setup_kwargs = {
    'name': 's3-loader',
    'version': '1.1.1',
    'description': 'wrapper script for uploading files and dirs to s3',
    'long_description': '# `s3-loader`\n\n**Install**\n```console\npip install s3-loader\n```\n\n**Usage**:\n\n```console\n$ s3-loader [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `auth`: to set aws credetials\n* `empty-bucket`: delete everything in an s3 bucket\n* `upload-dir`: upload an entire directory to s3\n* `upload-file`: upload a single file to s3\n\n## `s3-loader auth`\n\nto set aws credetials\n\n**Usage**:\n\n```console\n$ s3-loader auth [OPTIONS]\n```\n\n**Options**:\n\n* `--aws-access-key-id TEXT`: Your aws access key  [required]\n* `--aws-secret-access-key TEXT`: Your aws secret acess key  [required]\n* `--help`: Show this message and exit.\n\n## `s3-loader empty-bucket`\n\ndelete everything in an s3 bucket\n\n**Usage**:\n\n```console\n$ s3-loader empty-bucket [OPTIONS]\n```\n\n**Options**:\n\n* `--bucket-name TEXT`: Your bucket name  [required]\n* `--help`: Show this message and exit.\n\n## `s3-loader upload-dir`\n\nupload an entire directory to s3\n\n**Usage**:\n\n```console\n$ s3-loader upload-dir [OPTIONS]\n```\n\n**Options**:\n\n* `--path TEXT`: Path to your directory  [required]\n* `--bucket-name TEXT`: Your bucket name  [required]\n* `--help`: Show this message and exit.\n\n## `s3-loader upload-file`\n\nupload a single file to s3\n\n**Usage**:\n\n```console\n$ s3-loader upload-file [OPTIONS]\n```\n\n**Options**:\n\n* `--local-file TEXT`: Local file name  [required]\n* `--bucket TEXT`: Your bucket name  [required]\n* `--s3-file TEXT`: Name the file will use on s3  [required]\n* `--help`: Show this message and exit.\n',
    'author': 'phil-bell',
    'author_email': 'philhabell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phil-bell/s3-loader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.12,<4.0.0',
}


setup(**setup_kwargs)
