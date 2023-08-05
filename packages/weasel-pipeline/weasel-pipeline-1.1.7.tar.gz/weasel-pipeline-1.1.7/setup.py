# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_pipeline']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.7.1,<7.0.0',
 'configargparse>=1.2.3,<2.0.0',
 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'weasel-pipeline',
    'version': '1.1.7',
    'description': 'A minimalist pipelining framework for the WEASEL project.',
    'long_description': 'WEASEL Pipeline\n===============\n\n[![pipeline status](https://gitlab.com/weasel-project/weasel-pipeline/badges/master/pipeline.svg)](https://gitlab.com/weasel-project/weasel-pipeline/-/commits/master)\n[![PyPI version](https://img.shields.io/pypi/v/weasel-pipeline)](https://pypi.org/project/weasel-pipeline/)\n[![Documentation](https://readthedocs.org/projects/weasel-pipeline/badge/?version=latest&style=flat)](https://weasel-pipeline.readthedocs.io/en/latest/)\n[![dependency status](https://img.shields.io/librariesio/release/pypi/weasel-pipeline)](https://libraries.io/pypi/weasel-pipeline)\n![PyPI license](https://img.shields.io/pypi/l/weasel-pipeline)\n![PyPI Python version](https://img.shields.io/pypi/pyversions/weasel-pipeline)\n\n`weasel-pipeline` is a minimalist pipelining framework that serves as a common foundation of our scanning and data processing tool chains.\n\nInstallation instructions, examples, and further documentation available [here](https://weasel-pipeline.readthedocs.io/en/latest/).',
    'author': 'Fabian Marquardt',
    'author_email': 'marquard@cs.uni-bonn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/weasel-project/weasel-pipeline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
