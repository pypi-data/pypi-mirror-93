# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anlearn']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'scikit-learn>=0.23.0,<0.24.0', 'scipy>=1.5.0,<2.0.0']

extras_require = \
{'docs': ['matplotlib>=3.3.4,<4.0.0',
          'pandas>=1.0.0,<2.0.0',
          'Pillow>=8.1.0,<9.0.0',
          'Sphinx>=3.4.3,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'sphinx-gallery>=0.8.2,<0.9.0',
          'umap-learn>=0.5.0,<0.6.0']}

setup_kwargs = {
    'name': 'anlearn',
    'version': '0.1.3',
    'description': 'Anomaly learn - the anomaly detection package',
    'long_description': '![anomaly-learn-with-text](https://raw.githubusercontent.com/gaussalgo/anlearn/master/docs/img/anomaly-learn-with-text.png)\n\n[![PyPI version](https://badge.fury.io/py/anlearn.svg)](https://badge.fury.io/py/anlearn) [![Documentation Status](https://readthedocs.org/projects/anlearn/badge/?version=latest)](https://anlearn.readthedocs.io/en/latest/?badge=latest) [![Gitter](https://badges.gitter.im/gaussalgo-anlearn/community.svg)](https://gitter.im/gaussalgo-anlearn/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)\n\n# anlearn - Anomaly learn\n\nIn [Gauss Algorithmic], we\'re working on many anomaly/fraud detection projects using open-source tools. We decided to put our two cents in and  "tidy up" some of our code snippets, add documentation, examples, and release them as an open-source package. So let me introduce **anlearn**. It aims to offer multiple interesting anomaly detection methods in familiar [scikit-learn] API so you could quickly try some anomaly detection experiments yourself.\n\nSo far, this package is an alpha state and ready for your experiments.\n\nDo you have any questions, suggestions, or want to chat? Feel free to contact us via [Github], [Gitter], or email.\n\n## Installation\nanlearn depends on [scikit-learn] and it\'s dependencies [scipy] and [numpy].\n\nRequirements:\n* python >=3.6\n* [scikit-learn]\n* [scipy]\n* [numpy]\n\nRequirements for every supported python version with version and hashes could be found in `requirements` folder.\nWe\'re using [pip-tools] for generating requirements files.\n\n\n### Intallation options\n#### PyPI installation\n```\npip install anlearn\n```\n\n#### Installation from source\n```\ngit clone https://github.com/gaussalgo/anlearn\ncd anlearn\n```\n\nInstalil `anlearn`.\n```\npip install .\n```\nor by using [poetry]\n```\npoetry install\n```\n\n\n## Documentation\nYou can find documentation at Read the Docs: [docs](https://anlearn.readthedocs.io/en/latest/).\n\n## Contat us\nDo you have any questions, suggestions, or want to chat? Feel free to contact us via [Github], [Gitter], or email.\n\n## License\nGNU Lesser General Public License v3 or later (LGPLv3+)\n\nanlearn  Copyright (C) 2020  Gauss Algorithmic a.s.\n\nThis package is in alpha state and comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to use, redistribute it, and contribute under certain conditions of its license.\n\n# Code of Conduct\n[Code of Conduct](https://github.com/gaussalgo/anlearn/blob/master/CODE_OF_CONDUCT.md)\n\n\n[scikit-learn]: https://github.com/scikit-learn/scikit-learn\n[numpy]: https://github.com/numpy/numpy\n[scipy]: https://github.com/scipy/scipy\n[pip-tools]: https://github.com/jazzband/pip-tools\n[Gitter]: https://gitter.im/gaussalgo-anlearn/community\n[Gauss Algorithmic]: https://www.gaussalgo.com/en/\n[GitHub]: https://github.com/gaussalgo/anlearn\n[poetry]: https://github.com/python-poetry/poetry\n',
    'author': 'Ondrej Kurák',
    'author_email': 'kurak@gaussalgo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gaussalgo/anlearn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
