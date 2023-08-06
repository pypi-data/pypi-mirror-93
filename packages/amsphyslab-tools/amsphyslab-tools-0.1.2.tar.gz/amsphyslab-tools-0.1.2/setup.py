# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amsphyslab_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['amsphyslab = amsphyslab_tools.tools_cli:main']}

setup_kwargs = {
    'name': 'amsphyslab-tools',
    'version': '0.1.2',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
