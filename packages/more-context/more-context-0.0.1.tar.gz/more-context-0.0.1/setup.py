# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['more_context']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'more-context',
    'version': '0.0.1',
    'description': 'More Context',
    'long_description': '# More Context\n\nContext utilities\n\n## Installation\n\n    pip install more-context\n\n\n## Usage\n\n### Safe Context Manager\n\nLike `@contextmanager`, but safe.\n\nCode like this:\n\n```python\n@safe_context_manager\ndef my_ctx():\n    lock = lock_resource()\n    yield\n    lock.delete()\n```\n\nIs equivalent to:\n\n```python\n@contextmanager\ndef my_ctx():\n    lock = lock_resource()\n    try:\n        yield\n    finally:\n        lock.delete()\n```\n',
    'author': 'David Sternlicht',
    'author_email': 'd1618033@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d1618033/more-context',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
