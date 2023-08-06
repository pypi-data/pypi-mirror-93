# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package',
 'package.inference',
 'package.inference.serving_app',
 'package.inference.serving_app.service',
 'package.inference.serving_app.serving',
 'package.inference.serving_app.serving.v1',
 'package.inference.serving_app.serving.v2']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'gunicorn>=20.0.4,<21.0.0',
 'sentry_sdk>=0.19.5,<0.20.0',
 'starlette-prometheus>=0.7.0,<0.8.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'aicloud-deploy',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Toolkit AI Cloud для написания скриптов деплоя в Inference\n\n',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbercloud-ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
