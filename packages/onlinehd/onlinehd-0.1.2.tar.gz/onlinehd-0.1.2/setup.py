# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onlinehd']

package_data = \
{'': ['*'], 'onlinehd': ['fasthd/*']}

install_requires = \
['ninja>=1.10.0,<2.0.0', 'torch>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'onlinehd',
    'version': '0.1.2',
    'description': 'Efficient single-pass hyperdimensional classifier',
    'long_description': '# onlinehd\n\n**Authors**: Alejandro Hernández Cano, Mohsen Imani.\n\n## Installation\n\nIn order to install the package, simply run the following:\n\n```\npip install onlinehd\n```\n\nVisit the PyPI [project page](https://pypi.org/project/onlinehd/) for\nmore information about releases.\n\n## Documentation\n\nRead the [documentation](https://onlinehd.readthedocs.io/en/latest/)\nof this project. \n\n## Quick start\n\nThe following code generates dummy data and trains a OnlnineHD classification\nmodel with it.\n\n```python\n>>> import onlinehd\n>>> dim = 10000\n>>> n_samples = 1000\n>>> features = 100\n>>> classes = 5\n>>> x = torch.randn(n_samples, features) # dummy data\n>>> y = torch.randint(0, classes, [n_samples]) # dummy data\n>>> model = onlinehd.OnlineHD(classes, features, dim=dim)\n>>> if torch.cuda.is_available():\n...     print(\'Training on GPU!\')\n...     model = model.to(\'cuda\')\n...     x = x.to(\'cuda\')\n...     y = y.to(\'cuda\')\n...\nTraining on GPU!\n>>> model.fit(x, y, epochs=10)\n>>> ypred = model(x)\n>>> ypred.size()\ntorch.Size([1000])\n```\n\nFor more examples, see the `example.py` script. Be aware that this script needs\n`pytorch`, `sklearn` and `numpy` to run.\n\n## Citation Request\n\nIf you use onlinehd code, please cite the following paper:\n\n1. Alejandro Hernández-Cano, Namiko Matsumoto, Eric Ping, Mohsen Imani\n   "OnlineHD: Robust, Efficient, and Single-Pass Online Learning Using\n   Hyperdimensional System", IEEE/ACM Design Automation and Test in Europe\n   Conference\xa0(DATE), 2021.\n',
    'author': 'alehd',
    'author_email': 'ale.hdz333@ciencias.unam.mx',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/biaslab/onlinehd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
