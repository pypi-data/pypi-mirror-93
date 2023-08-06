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
    'version': '1.1.0',
    'description': 'wrapper script for uploading files and dirs to s3',
    'long_description': '# `s3-loader`\n\n**Install**\n```console\npip install s3-loader\n```\n\n**Usage**:\n\n```console\n$ s3-loader [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `auth`: authenticate with your aws access key and...\n* `clear-bucket`: delete everything in an s3 bucket\n* `upload-dir`: upload an entire directory to s3\n* `upload-file`: upload a single file to s3\n\n## `s3-loader auth`\n\nauthenticate with your aws access key and secret\n\n**Usage**:\n\n```console\n$ s3-loader auth [OPTIONS] [AWS_ACCESS_KEY_ID] [AWS_SECRET_ACCESS_KEY]\n```\n\n**Arguments**:\n\n* `[AWS_ACCESS_KEY_ID]`: Your aws access key  [default: ]\n* `[AWS_SECRET_ACCESS_KEY]`: Your aws secret acess ket  [default: ]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `s3-loader clear-bucket`\n\ndelete everything in an s3 bucket\n\n**Usage**:\n\n```console\n$ s3-loader clear-bucket [OPTIONS] [BUCKET_NAME]\n```\n\n**Arguments**:\n\n* `[BUCKET_NAME]`: Your bucket name  [default: ]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `s3-loader upload-dir`\n\nupload an entire directory to s3\n\n**Usage**:\n\n```console\n$ s3-loader upload-dir [OPTIONS] [PATH] [BUCKET_NAME]\n```\n\n**Arguments**:\n\n* `[PATH]`: Path to your directory  [default: ]\n* `[BUCKET_NAME]`: Your bucket name  [default: ]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `s3-loader upload-file`\n\nupload a single file to s3\n\n**Usage**:\n\n```console\n$ s3-loader upload-file [OPTIONS] [LOCAL_FILE] [BUCKET] [S3_FILE]\n```\n\n**Arguments**:\n\n* `[LOCAL_FILE]`: Local file name  [default: ]\n* `[BUCKET]`: Your bucket name  [default: ]\n* `[S3_FILE]`: Name the file will use on s3  [default: ]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
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
