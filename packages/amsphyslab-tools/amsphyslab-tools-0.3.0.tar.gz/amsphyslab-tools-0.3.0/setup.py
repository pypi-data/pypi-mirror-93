# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amsphyslab_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'packaging>=19,<21']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.17,<3.0.0']}

entry_points = \
{'console_scripts': ['amsphyslab-env = amsphyslab_tools.tools_cli:main']}

setup_kwargs = {
    'name': 'amsphyslab-tools',
    'version': '0.3.0',
    'description': 'Tools used for physics practicals at the Amsterdam universities.',
    'long_description': '# amsphyslab-tools\n Tools used for physics practicals at the Amsterdam universities.\n',
    'author': 'David Fokkema',
    'author_email': 'davidfokkema@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
