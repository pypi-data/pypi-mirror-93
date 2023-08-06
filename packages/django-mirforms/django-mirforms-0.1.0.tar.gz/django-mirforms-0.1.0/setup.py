# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirforms']

package_data = \
{'': ['*'], 'mirforms': ['templates/mirforms/widgets/htmx_select/*']}

install_requires = \
['cryptocode>=0.1,<0.2']

setup_kwargs = {
    'name': 'django-mirforms',
    'version': '0.1.0',
    'description': 'A Django app contains custom html form inputs.',
    'long_description': '=====\nmirforms\n=====\n\nMir forms is a Django app contains custom html form inputs.\n\nQuick start\n-----------\n\n1. Add "mirforms" to your INSTALLED_APPS setting like this::\n\n    INSTALLED_APPS = [\n        ...\n        \'mirforms\',\n    ]\n\n2. Include the mirforms URLconf in your project urls.py like this::\n\n    path(\'mirforms/\', include(\'mirforms.urls\')),',
    'author': 'Abidar El Mehdi',
    'author_email': 'abidar.elmehdi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abidarelmehdi/django-mirforms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
