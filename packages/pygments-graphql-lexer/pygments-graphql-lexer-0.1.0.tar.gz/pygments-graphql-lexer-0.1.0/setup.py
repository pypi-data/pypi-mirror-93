# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphqllexer']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.2,<3.0.0']

entry_points = \
{'pygments.lexers': ['graphqllexer = graphqllexer.lexer:GraphqlLexer']}

setup_kwargs = {
    'name': 'pygments-graphql-lexer',
    'version': '0.1.0',
    'description': 'GraphQL lexer for Pygments',
    'long_description': None,
    'author': 'Gazorby',
    'author_email': 'gazorby@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
