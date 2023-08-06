# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowdyn', 'flowdyn.modelphy', 'flowdyn.solution']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.3', 'numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'flowdyn',
    'version': '1.0.1',
    'description': 'Model of discretization of hyperbolic model, base is Finite Volume method',
    'long_description': None,
    'author': 'j.gressier',
    'author_email': 'jeremie.gressier@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
