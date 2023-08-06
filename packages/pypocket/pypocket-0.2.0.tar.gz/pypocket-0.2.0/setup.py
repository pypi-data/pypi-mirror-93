# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypocket', 'pypocket.test']

package_data = \
{'': ['*']}

install_requires = \
['dominate>=2.6.0,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pypocket',
    'version': '0.2.0',
    'description': 'A Python wrapper for GetPocket',
    'long_description': '# PyPocket\n\n![](https://img.shields.io/badge/Project%20Status-Under%20Development-green)\n\n[![Actions Status](https://github.com/e-alizadeh/pypocket/workflows/Build%20and%20Test/badge.svg?feature=master)](https://github.com/e-alizadeh/pypocket/actions)\n[![PyPI version](https://badge.fury.io/py/pypocket.svg)](https://badge.fury.io/py/pypocket)\n![MIT License](https://img.shields.io/badge/License-MIT-blueviolet)\n[![Code Style: Black](https://img.shields.io/badge/Code%20style-black-black)](https://github.com/psf/black)\n \n\n---\n[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/dashboard?id=PyPocket)\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=coverage)](https://sonarcloud.io/dashboard?id=PyPocket)\n[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=security_rating)](https://sonarcloud.io/dashboard?id=PyPocket)\n[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=PyPocket)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=PyPocket)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=PyPocket)\n[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=PyPocket&metric=ncloc)](https://sonarcloud.io/dashboard?id=PyPocket)\n---\n\nA Python Package for GetPocket (https://getpocket.com)\n\n\n## Installation\n```bash\npip install pypocket\n```\n\n## Library Requirements\n- requests\n- dominate\n\n---\n## Prerequisite: Obtain Your Consumer Key & Access Token\nIn order to use PyPocket, you will need consumer_key and access_token for your Pocket. \nFor the consumer_key, you can follow Step 1 of [Pocket Authentication API Documentation](https://getpocket.com/developer/docs/authentication)\nto obtain your consumer_key. \n\nFor obtaining your access_token, you can either follow the pocket documentation (above link) to get your access_token,\nor use the `Auth` class available in this library for your convenience as below. \n```python\nfrom pypocket.auth import Auth\nauth = Auth(consumer_key="your_consumer_key")\n# The following will automatically obtain a request_token and ask you to authorize it. \nauth.authorize_request_token_browser() \n```\n\nThe `auth.authorize_request_token_browser()` will open a webpage to getpocket.com website asking  you to authorize the token. \nOnce, you authorize it. Then you can get your access token by running the following:\n```python\naccess_token = auth.get_access_token() \n```\n---\n## Usage\n\n```python\nfrom pypocket import Pocket\n\np =  Pocket(\n    consumer_key="your_consumer_key", \n    access_token="your_token", \n    html_filename="report"\n)\np.to_html(num_post=10)\n```\n---\n\nCheck the development roadmap for this project [here](https://github.com/e-alizadeh/PyPocket/projects/1)\n\n\n## New features in the pipeline\n- Retrieve pocket contents according to given tags\n- Modify the pocket contents properties\n',
    'author': 'Essi Alizadeh',
    'author_email': 'pypocket@ealizadeh.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/e-alizadeh/PyPocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
