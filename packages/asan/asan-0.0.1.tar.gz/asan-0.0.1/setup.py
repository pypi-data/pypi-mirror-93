# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asan']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.63,<2.0.0', 'click>=7.1.2,<8.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'asan',
    'version': '0.0.1',
    'description': 'The AWS Swiss Army Knife is a small tool that helps with various small tasks',
    'long_description': 'AWS Swiss Army Knife\n====================\n\nThis is a small tool for common aws tasks.\n\nThere will be multiple sections here\n',
    'author': 'Eduard Thamm',
    'author_email': 'eduard.thamm@thammit.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/edthamm/aws-swiss-army-knife',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
