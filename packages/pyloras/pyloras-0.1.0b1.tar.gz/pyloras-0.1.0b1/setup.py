# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloras']

package_data = \
{'': ['*']}

install_requires = \
['imbalanced-learn>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'pyloras',
    'version': '0.1.0b1',
    'description': 'LoRAS: An oversampling approach for imbalanced datasets',
    'long_description': "# LoRAS\nLocalized Random Affine Shadowsampling\n\nThis repo provides a python implementation of an imbalanced dataset oversampling\ntechnique known as Localized Random Affine Shadowsampling (LoRAS). This implementation \npiggybacks off the package ``imbalanced-learn`` and thus aims to be as compatible\nas possible with it.\n\n\n## Dependencies\n- `imbalanced-learn`\n\n\n## Installation\n\nInstallation requires an installation of [poetry][1] and the following shell commands:\n\n```shell\n$ git clone https://github.com/zoj613/pyloras.git\n$ cd pyloras/\n$ poetry install\n# add package to python's path\n$ export PYTHONPATH=$PWD:$PYTHONPATH \n```\n\n## Usage\n\n```python\nfrom collections import Counter\nfrom pyloras import LORAS\nfrom sklearn.datasets import make_classification\n\nX, y = make_classification(n_samples=5000, n_features=2, n_informative=2,\n                           n_redundant=0, n_repeated=0, n_classes=3,\n                           n_clusters_per_class=1,\n                           weights=[0.01, 0.05, 0.94],\n                           class_sep=0.8, random_state=0)\n\nlrs = LORAS(random_state=0, embedding_params={'init':'pca', 'n_iter':250})\nX_resampled, y_resampled = lrs.fit_resample(X, y)\nprint(sorted(Counter(y_resampled).items()))\n[(0, 4672), (1, 4454), (2, 4674)]\n```\n\n## References\nBej, S., Davtyan, N., Wolfien, M. et al. LoRAS: an oversampling approach for imbalanced datasets. Mach Learn 110, 279–301 (2021). https://doi.org/10.1007/s10994-020-05913-4\n\n\n[1]: https://python-poetry.org/docs/pyproject/\n",
    'author': 'Zolisa Bleki',
    'author_email': 'zolisa.bleki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
