# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dorado',
 'dorado.scheduling',
 'dorado.scheduling.constraints',
 'dorado.scheduling.data',
 'dorado.scheduling.scripts',
 'dorado.scheduling.tests']

package_data = \
{'': ['*']}

install_requires = \
['astroplan>=0.7',
 'astropy>=4.1,<5.0',
 'cplex',
 'docplex',
 'healpy',
 'ligo.skymap>=0.5.0,<0.6.0',
 'numpy<1.20.0',
 'seaborn',
 'shapely',
 'skyfield']

entry_points = \
{'console_scripts': ['dorado-scheduling = dorado.scheduling.scripts.main:main',
                     'dorado-scheduling-animate = '
                     'dorado.scheduling.scripts.animate:main']}

setup_kwargs = {
    'name': 'dorado-scheduling',
    'version': '0.1.0',
    'description': 'Dorado observation planning and scheduling simulations',
    'long_description': None,
    'author': 'Leo Singer',
    'author_email': 'leo.singer@ligo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
