# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wihmt']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'dash>=1.19.0,<2.0.0',
 'ofxtools>=0.9.1,<0.10.0',
 'pandas>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['wihmt = wihmt.__main__:main']}

setup_kwargs = {
    'name': 'wihmt',
    'version': '0.1.0',
    'description': 'Will I have money tomorrow',
    'long_description': "Will I have money tomorrow\n==========================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/wihmt.svg\n   :target: https://pypi.org/project/wihmt/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/wihmt\n   :target: https://pypi.org/project/wihmt\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/wihmt\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/wihmt/latest.svg?label=Read%20the%20Docs\n   :target: https://wihmt.readthedocs.io/\n   :alt: Read the documentation at https://wihmt.readthedocs.io/\n.. |Tests| image:: https://github.com/asteroide/wihmt/workflows/Tests/badge.svg\n   :target: https://github.com/asteroide/wihmt/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/asteroide/wihmt/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/asteroide/wihmt\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Will I have money tomorrow* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install wihmt\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Will I have money tomorrow* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/asteroide/wihmt/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://wihmt.readthedocs.io/en/latest/usage.html\n",
    'author': 'Asteroide',
    'author_email': 'asteroide@domtombox.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asteroide/wihmt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
