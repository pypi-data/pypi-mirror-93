# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edfi_google_classroom_extractor',
 'edfi_google_classroom_extractor.api',
 'edfi_google_classroom_extractor.helpers',
 'edfi_google_classroom_extractor.mapping']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'SQLAlchemy>=1.3.19,<2.0.0',
 'edfi-lms-extractor-lib==1.0.0a0',
 'errorhandler>=2.0.1,<3.0.0',
 'google-api-python-client>=1.11.0,<2.0.0',
 'google-auth-oauthlib>=0.4.1,<0.5.0',
 'numpy==1.19.3',
 'opnieuw>=1.1.0,<2.0.0',
 'pandas>=1.1.1,<2.0.0',
 'pytest>=6.0,<7.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'tail-recursive>=2.0.0,<3.0.0',
 'teamcity-messages>=1.28,<2.0',
 'xxhash>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'edfi-google-classroom-extractor',
    'version': '1.0.0a0',
    'description': 'Extract tool for retrieving student data from Google Classroom',
    'long_description': None,
    'author': 'Ed-Fi Alliance, LLC, and contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://techdocs.ed-fi.org/display/EDFITOOLS/LMS+Toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
