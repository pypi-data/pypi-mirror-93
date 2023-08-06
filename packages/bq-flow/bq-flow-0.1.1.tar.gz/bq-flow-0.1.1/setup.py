# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bqflow']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'abq>=0.1.1,<0.2.0',
 'click>=7.1.2,<8.0.0',
 'pydantic[dotenv]>=1.7.3,<2.0.0',
 'sqlparse>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['bqflow = bqflow.main:cmd']}

setup_kwargs = {
    'name': 'bq-flow',
    'version': '0.1.1',
    'description': 'BigQuery Workflow',
    'long_description': None,
    'author': 'sakuv2',
    'author_email': 'loots2438@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
