# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vatglobaldevopsinterview']

package_data = \
{'': ['*']}

install_requires = \
['Django==3.1.5',
 'Jinja2==2.11.2',
 'Markdown==3.3.3',
 'MarkupSafe==1.1.1',
 'arrow==0.17.0',
 'asgiref==3.3.1',
 'blessed==1.17.12',
 'certifi==2020.12.5',
 'chardet==4.0.0',
 'coreapi==2.3.3',
 'coreschema==0.0.4',
 'django-cors-headers==3.7.0',
 'django-filter==2.4.0',
 'django-picklefield==3.0.1',
 'django-q==1.3.4',
 'django-rest==0.8.6',
 'django>=3.1.5,<4.0.0',
 'djangorestframework-camel-case==1.2.0',
 'djangorestframework==3.12.2',
 'drf-yasg==1.20.0',
 'idna==2.10',
 'inflection==0.5.1',
 'itypes==1.2.0',
 'markdown>=3.3.3,<4.0.0',
 'names==0.3.0',
 'packaging==20.8',
 'psutil==5.8.0',
 'pyparsing==2.4.7',
 'python-dateutil==2.8.1',
 'pytz==2020.5',
 'requests==2.25.1',
 'ruamel.yaml.clib==0.2.2',
 'ruamel.yaml==0.16.12',
 'six==1.15.0',
 'sqlparse==0.4.1',
 'uritemplate==3.0.1',
 'urllib3==1.26.2',
 'wcwidth==0.2.5']

setup_kwargs = {
    'name': 'vatglobaldevopsinterview',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Christo Goosen',
    'author_email': 'christogoosen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
