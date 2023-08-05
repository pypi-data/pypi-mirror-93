# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydebuginfod']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pydebuginfod',
    'version': '0.0.1',
    'description': 'A python client for the debuginfod server',
    'long_description': '# pydebuginfod\n\npydebuginfod is a Python client implementation of the [debuginfod\nspec](https://www.mankier.com/8/debuginfod).\n\n```python\nimport pydebuginfod\n\ndbginfo = pydebuginfod.get_debuginfo("c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b")\ndbginfo\n>>> \'/home/matt/.cache/debuginfod/buildid/c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b/debuginfo\'\n\nexecutable = debuginfod.get_executable("c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b")\ndbginfo\n>>> \'/home/matt/.cache/debuginfod/buildid/c0e8c127f1f36dd10e77331f46b6e2dbbbdb219b/executable\'\n```\n\npydebuginfod allows you to easily get started with debuginfod.',
    'author': 'Matt Schulte',
    'author_email': 'schultetwin1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
