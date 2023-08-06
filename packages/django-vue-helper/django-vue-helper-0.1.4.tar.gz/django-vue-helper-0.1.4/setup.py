# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vue_helper', 'vue_helper.templatetags', 'vue_helper.tests']

package_data = \
{'': ['*'], 'vue_helper': ['templates/vue_helper/*']}

install_requires = \
['django>=2.2,<=3.2']

setup_kwargs = {
    'name': 'django-vue-helper',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
