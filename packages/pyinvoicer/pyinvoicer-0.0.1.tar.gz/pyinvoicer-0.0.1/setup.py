# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinvoicer']

package_data = \
{'': ['*'], 'pyinvoicer': ['templates/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'PyYAML>=5.4.1,<6.0.0', 'WeasyPrint>=52.2,<53.0']

entry_points = \
{'console_scripts': ['invoicer = pyinvoicer.pyinvoicer:main']}

setup_kwargs = {
    'name': 'pyinvoicer',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Taihsiang Ho (tai271828)',
    'author_email': 'tai271828@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
