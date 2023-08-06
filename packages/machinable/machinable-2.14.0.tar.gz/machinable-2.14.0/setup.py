# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['machinable',
 'machinable.config',
 'machinable.console',
 'machinable.console.vendor',
 'machinable.core',
 'machinable.engine',
 'machinable.execution',
 'machinable.experiment',
 'machinable.filesystem',
 'machinable.index',
 'machinable.project',
 'machinable.project.export',
 'machinable.registration',
 'machinable.server',
 'machinable.server.graphql',
 'machinable.server.graphql.types',
 'machinable.server.graphql.types.mutation',
 'machinable.server.graphql.types.query',
 'machinable.server.graphql.types.subscription',
 'machinable.storage',
 'machinable.submission',
 'machinable.submission.collections',
 'machinable.submission.models',
 'machinable.submission.views',
 'machinable.utils']

package_data = \
{'': ['*'], 'machinable.server.graphql': ['schema/*']}

install_requires = \
['GitPython>=3.1,<4.0',
 'PyYAML>=5.3,<6.0',
 'click>=7.1,<8.0',
 'dotmap>=1.3,<2.0',
 'expandvars>=0.6,<0.7',
 'flatten-dict>=0.3,<0.4',
 'fs>=2.4,<3.0',
 'igittigitt>=2.0,<3.0',
 'jsonlines>=1.2,<2.0',
 'observable>=1.0,<2.0',
 'pendulum>=2.1,<3.0',
 'python-baseconv>=1.2,<2.0',
 'regex==2020.7.14',
 'setproctitle>=1.1,<2.0',
 'sh>=1.13,<2.0']

extras_require = \
{'integrations': ['numpy>=1.19.4,<2.0.0',
                  'ray[tune]>=1.0.1,<2.0.0',
                  'deepdiff>=5.0.2,<6.0.0',
                  'pandas>=1.1.5,<2.0.0',
                  'tabulate>=0.8.7,<0.9.0',
                  'dataset>=1.4.1,<2.0.0'],
 'server': ['ariadne>=0.12.0,<0.13.0', 'uvicorn>=0.13.1,<0.14.0']}

entry_points = \
{'console_scripts': ['machinable = machinable.console.cli:cli']}

setup_kwargs = {
    'name': 'machinable',
    'version': '2.14.0',
    'description': 'A modular platform for machine learning projects',
    'long_description': '<div align="center">\n  <img src="https://raw.githubusercontent.com/machinable-org/machinable/master/docs/logo/logo.png">\n</div>\n\n# machinable\n\n<a href="https://travis-ci.org/machinable-org/machinable">\n<img src="https://travis-ci.org/machinable-org/machinable.svg?branch=master" alt="Build Status">\n</a>\n<a href="https://opensource.org/licenses/MIT">\n<img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">\n</a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n\n<br />\n<br />\n\n**machinable** provides a system to manage configuration of machine learning projects more effectively. Using straight-forward conventions and a powerful configuration engine, it can help structure your projects in a principled way so you can move quickly while enabling reuse and collaboration.\n\nRead the [user guide ](https://machinable.org/guide) to get started.\n\n## Features\n\n**Powerful configuration**\n\n- YAML-based project-wide configuration files with expressive syntax\n- Efficient configuration manipulation\n- Modular code organisation to allow for encapsulation and re-use\n- Import system to use 3rd party configuration and code without overhead\n- \'Mixins\' for horizontal inheritance structure\n\n**Efficient execution**\n\n- Works with existing code\n- Support for seamless cloud execution\n- Automatic code backups\n- Managed randomness and reproducibility\n- Advanced hyperparameter tuning using [Ray Tune](https://github.com/ray-project/ray)\n\n**Effective result collection and analysis**\n\n- Logging, tabular record writer and storage API\n- File system abstraction (in-memory, AWS S3, and more)\n- Flat-file result database with convenient query syntax\n\n',
    'author': 'Frithjof Gressmann',
    'author_email': 'hello@machinable.org',
    'maintainer': 'Frithjof Gressmann',
    'maintainer_email': 'hello@machinable.org',
    'url': 'https://machinable.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
