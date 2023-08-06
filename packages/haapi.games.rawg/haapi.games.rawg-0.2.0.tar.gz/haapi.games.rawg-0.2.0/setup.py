# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['haapi', 'haapi.games.rawg', 'haapi.games.rawg.objects']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0', 'desert>=2020.11.18,<2021.0.0']

setup_kwargs = {
    'name': 'haapi.games.rawg',
    'version': '0.2.0',
    'description': 'Haapi Games Rawg',
    'long_description': "Haapi Games Rawg\n================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/haapi.games.rawg.svg\n   :target: https://pypi.org/project/haapi.games.rawg/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/haapi.games.rawg\n   :target: https://pypi.org/project/haapi.games.rawg\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/haapi.games.rawg\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/haapigamesrawg/latest.svg?label=Read%20the%20Docs\n   :target: https://haapigamesrawg.readthedocs.io/\n   :alt: Read the documentation at https://haapigamesrawg.readthedocs.io/\n.. |Tests| image:: https://github.com/Haapi-Games/haapi.games.rawg/workflows/Tests/badge.svg\n   :target: https://github.com/Haapi-Games/haapi.games.rawg/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/Haapi-Games/haapi.games.rawg/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/Haapi-Games/haapi.games.rawg\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nInstallation\n------------\n\nYou can install *Haapi Games Rawg* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install haapi.games.rawg\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Haapi Games Rawg* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/Haapi-Games/haapi.games.rawg/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://haapigamesrawg.readthedocs.io/en/latest/usage.html\n",
    'author': 'Haapi',
    'author_email': 'haapigeek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Haapi-Games/haapi.games.rawg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
