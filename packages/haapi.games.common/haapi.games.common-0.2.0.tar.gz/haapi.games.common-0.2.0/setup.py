# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['haapi', 'haapi.games.common', 'haapi.games.common.gcp']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-secret-manager>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'haapi.games.common',
    'version': '0.2.0',
    'description': 'Haapi Games Common',
    'long_description': "Haapi Games Common\n==================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/haapi.games.common.svg\n   :target: https://pypi.org/project/haapi.games.common/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/haapi.games.common\n   :target: https://pypi.org/project/haapi.games.common\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/haapi.games.common\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/haapigamescommon/latest.svg?label=Read%20the%20Docs\n   :target: https://haapigamescommon.readthedocs.io/\n   :alt: Read the documentation at https://haapigamescommon.readthedocs.io/\n.. |Tests| image:: https://github.com/Haapi-Games/haapi.games.common/workflows/Tests/badge.svg\n   :target: https://github.com/Haapi-Games/haapi.games.common/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/Haapi-Games/haapi.games.common/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/Haapi-Games/haapi.games.common\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* Generic ``get_config`` function for projects\n* Common ``SecretManager`` for GCP secrets\n\n\nRequirements\n------------\n\n* Python>3.6.1\n\n\nInstallation\n------------\n\nYou can install *Haapi Games Common* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install haapi.games.common\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Haapi Games Common* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/Haapi-Games/haapi.games.common/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://haapigamescommon.readthedocs.io/en/latest/usage.html\n",
    'author': 'Haapi',
    'author_email': 'haapigeek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Haapi-Games/haapi.games.common',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
