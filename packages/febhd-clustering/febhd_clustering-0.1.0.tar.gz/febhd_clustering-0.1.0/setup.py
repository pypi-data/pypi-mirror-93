# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['febhd_clustering']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'febhd-clustering',
    'version': '0.1.0',
    'description': 'Smart Hyperdimensional Clustering algorithm: FebHD',
    'long_description': '# hd-clustering\n\n**Authors**: Alejandro Hernández Cano, Mohsen Imani.\n\n## Installation\n\nIn order to install the package, simply run the following:\n\n```\npip install febhd_clustering\n```\n\nVisit the PyPI [project page](https://pypi.org/project/febhd_clustering/) for\nmore information about releases.\n\n## Documentation\n\nRead the [documentation](https://febhd_clustering.readthedocs.io/en/latest/)\nof this project. \n\n## Quick start\n\nThe following code generates dummy data and trains a FebHD clustering model\nwith it.\n\n```python\n>>> import febhd_clustering\n>>> dim = 10000\n>>> n_samples = 1000\n>>> features = 100\n>>> clusters = 5\n>>> x = torch.randn(n_samples, features) # dummy data\n>>> model = febhd_clustering.FebHD(clusters, features, dim=dim)\n>>> if torch.cuda.is_available():\n...     print(\'Training on GPU!\')\n...     model = model.to(\'cuda\')\n...     x = x.to(\'cuda\')\n...\nTraining on GPU!\n>>> model.fit(x, epochs=10)\n>>> ypred = model(x)\n>>> ypred.size()\ntorch.Size([1000])\n```\n\nFor more examples, see the `examples/` directory.\n\n## Citation request\n\nIf you use hd-clustering, please cite the following papers:\n\n1. Alejandro\xa0Hernández-Cano, Yeseong\xa0Kim, Mohsen Imani. "A Framework for\n   Efficient and Binary Clustering in High-Dimensional Space". IEEE/ACM Design\n   Automation and Test in Europe Conference\xa0(DATE), 2021.\n\n2. Mohsen Imani,\xa0et al. "DUAL: Acceleration of Clustering Algorithms using\n   Digital-based Processing In-Memory"r\xa0IEEE/ACM International Symposium on\n   Microarchitecture\xa0(MICRO), 2020.\n',
    'author': 'alehd',
    'author_email': 'ale.hdz333@ciencias.unam.mx',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/biaslab/hd-clustering',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
