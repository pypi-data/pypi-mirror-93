# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uwnet',
 'uwnet.analysis',
 'uwnet.criticism',
 'uwnet.data',
 'uwnet.ml_models',
 'uwnet.ml_models.nn',
 'uwnet.ml_models.sklearn_generic',
 'uwnet.wave',
 'uwnet.wave.plots']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'altair_saver>=0.5.0,<0.6.0',
 'attrs>=20.2.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'cython>=0.29.21,<0.30.0',
 'dask>=1.1',
 'f90nml>=1.2,<2.0',
 'flake8>=3.8.4,<4.0.0',
 'fsspec>=0.8.3,<0.9.0',
 'h5netcdf>=0.8.1,<0.9.0',
 'ipython>=7.18.1,<8.0.0',
 'joblib>=0.13',
 'jupyterlab>=2.2.8,<3.0.0',
 'matplotlib>=3.3',
 'metpy>=0.12.2,<0.13.0',
 'netcdf4>=1.4',
 'numpy>=1.16',
 'pymongo>=3.11.0,<4.0.0',
 'pytest>=6.1.1,<7.0.0',
 'pytorch-ignite>=0.4.2,<0.5.0',
 'recommonmark>=0.6.0,<0.7.0',
 'sacred>=0.8.1,<0.9.0',
 'scikit-learn>=0.20',
 'seaborn>=0.11.0,<0.12.0',
 'snakemake>=5.26.1,<6.0.0',
 'sphinx>=1.7',
 'sphinx_rtd_theme>=0.5.0,<0.6.0',
 'toolz>=0.11.1,<0.12.0',
 'torch>=1.0',
 'torchvision>=0.7.0,<0.8.0',
 'tqdm>=4.50.2,<5.0.0',
 'xarray>=0.12',
 'zarr>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'uwnet',
    'version': '0.9.1',
    'description': '',
    'long_description': None,
    'author': 'Noah D. Brenowitz',
    'author_email': 'nbren12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
