# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cert_human_py3']

package_data = \
{'': ['*']}

install_requires = \
['asn1crypto>=1.4,<2.0', 'pyOpenSSL>=20,<21']

setup_kwargs = {
    'name': 'cert-human-py3',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
