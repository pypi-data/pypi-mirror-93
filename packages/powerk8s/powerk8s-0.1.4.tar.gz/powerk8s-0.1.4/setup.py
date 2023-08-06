# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['powerk8s']
install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'kubernetes>=12.0.1,<13.0.0',
 'powerline-status>=2.7,<3.0']

entry_points = \
{'console_scripts': ['lint = scripts.lint:main']}

setup_kwargs = {
    'name': 'powerk8s',
    'version': '0.1.4',
    'description': 'Powerline Segment for Kubernetes',
    'long_description': None,
    'author': 'George Kontridze',
    'author_email': 'george.kontridze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
