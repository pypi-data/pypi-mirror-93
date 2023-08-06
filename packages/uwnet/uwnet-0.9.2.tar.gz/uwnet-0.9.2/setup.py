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
    'version': '0.9.2',
    'description': 'PyTorch training code for climate modeling',
    'long_description': '# Machine learning approaches to convective parametrization\n[![CircleCI](https://circleci.com/gh/VulcanClimateModeling/uwnet.svg?style=svg&circle-token=3c696b66d8dd0b789e012a14e93a6397c2cbe833)](https://circleci.com/gh/VulcanClimateModeling/uwnet)\n\n## Documentation\n\nThe documentation is hosted on github pages: https://nbren12.github.io/uwnet/\n\n## Setup\n\n## Obtaining permission to use SAM\n\nThe System for Atmospheric Modeling (SAM) is a key part of the pre-processing\npipeline and prognostic evaluation of this machine learning project, but it is\nnot necessary for offline evaluation or training.\n\nIf you want access to SAM, please email the author Marat Khairoutdinov (cc\'ing\nme) to ask for permission. Then, I can give you access to the slightly modified\nversion of SAM used for this project.\n\nOnce you have arranged this access, the SAM source code can be download to the\npath `ext/sam` using\n\n    git submodule --init --recursive\n\n\n\n## Setting up the environment\n\nThis project uses two dependency management systems. Docker is needed to run\nthe SAM model and SAM-related preprocessing steps. you do not need this if\nyou are only training a model from pre-processed data (the data in zenodo).\nPoetry is a simpler pure python solution that should work for most common scenarios.\n\nTo use docker, you first need to build the image:\n\n    make build_image\n\nIf you get an error `make: nvidia-docker: Command not found`, edit the\nMakefile to have `DOCKER = docker` instead of `nvidia-docker`. (Assuming\ndocker is already installed.) Then, the docker environment can be entered by\ntyping\n\n    make enter\n\nThis opens a shell variable in a docker container with all the necessary\nsoftware requirements.\n\nTo use poetry, you can install all the needed packages and enter a sandboxed\nenvironment by running\n\n    poetry install\n    poetry shell\n\nThe instructions below assume you are in one of these environments\n\n# Running the workflow\n\nTo run train the models, type\n    \n    snakemake -j <number of parallel jobs>\n\nThis will take a long time! To see all the steps and the corresponding commands\nin this workflow, type\n\n    snakemake -n -p\n\nThis whole analysis is specified in the Snakefile, which is the first place to\nlook.\n\nTo reproduce the plots for the Journal of Atmospheric science paper, run\n\n    make jas2020\n\nThe figures for this paper requires you to install\n[chromedriver](https://chromedriver.chromium.org/) to export to svg format. I\ndid this on my mac with these commands:\n\n    # for svg saving from altair\n    brew install chromedriver\n\n    # on mac os to allow unverified developers\n    xattr -d com.apple.quarantine /usr/local/bin/chromedriver\n\nYou also need to install Inkscape to convert the svg to pdf format.\n\n\n[docker]: https://www.docker.com/\n\n# Evaluating performance\n\nEvaluating ML Paramerizations is somewhat different than normal ML scoring.\nSome useful metrics which work for xarray data are available in\n`uwnet.metrics`. In particular `uwnet.metrics.r2_score` computes the ubiquitous\nR2 score.\n\n# Performing online tests\n\nSAM has been modified to call arbitrary python functions within it\'s time stepping loop. These python functions accept a dictionary of numpy arrays as inputs, and store output arrays with specific names to this dictionary. Then SAM will pull the output contents of this dictionary back into Fortran and apply any computed tendency. \n\nTo extend this, one first needs to write a suitable function, which can be tested using the data stored at `assets/sample_sam_state.pt`. The following steps explore this data\n\n```ipython\nIn [5]: state =  torch.load("assets/sample_sam_state.pt")                                                                                 \n\nIn [6]: state.keys()                                                                                                                      \nOut[6]: dict_keys([\'layer_mass\', \'p\', \'pi\', \'caseid\', \'case\', \'liquid_ice_static_energy\', \'_DIMS\', \'_ATTRIBUTES\', \'total_water_mixing_ratio\', \'air_temperature\', \'upward_air_velocity\', \'x_wind\', \'y_wind\', \'tendency_of_total_water_mixing_ratio_due_to_dynamics\', \'tendency_of_liquid_ice_static_energy_due_to_dynamics\', \'tendency_of_x_wind_due_to_dynamics\', \'tendency_of_y_wind_due_to_dynamics\', \'latitude\', \'longitude\', \'sea_surface_temperature\', \'surface_air_pressure\', \'toa_incoming_shortwave_flux\', \'surface_upward_sensible_heat_flux\', \'surface_upward_latent_heat_flux\', \'air_pressure\', \'air_pressure_on_interface_levels\', \'dt\', \'time\', \'day\', \'nstep\'])\n\nIn [7]: qt = state[\'total_water_mixing_ratio\']                                                                                            \n\nIn [8]: qt.shape                                                                                                                          \nOut[8]: (34, 64, 128)\n\nIn [9]: state[\'sea_surface_temperature\'].shape                                                                                            \nOut[9]: (1, 64, 128)\n\nIn [10]: state[\'air_pressure_on_interface_levels\'].shape                                                                                  \nOut[10]: (35,)\n\nIn [11]: state[\'p\'].shape                                                                                                                 \nOut[11]: (34,)\n\nIn [12]: state[\'_ATTRIBUTES\']                                                                                                             \nOut[12]: \n{\'liquid_ice_static_energy\': {\'units\': \'K\'},\n \'total_water_mixing_ratio\': {\'units\': \'g/kg\'},\n \'air_temperature\': {\'units\': \'K\'},\n \'upward_air_velocity\': {\'units\': \'m/s\'},\n \'x_wind\': {\'units\': \'m/s\'},\n \'y_wind\': {\'units\': \'m/s\'},\n \'tendency_of_total_water_mixing_ratio_due_to_dynamics\': {\'units\': \'m/s\'},\n \'tendency_of_liquid_ice_static_energy_due_to_dynamics\': {\'units\': \'m/s\'},\n \'tendency_of_x_wind_due_to_dynamics\': {\'units\': \'m/s\'},\n \'tendency_of_y_wind_due_to_dynamics\': {\'units\': \'m/s\'},\n \'latitude\': {\'units\': \'degreeN\'},\n \'longitude\': {\'units\': \'degreeN\'},\n \'sea_surface_temperature\': {\'units\': \'K\'},\n \'surface_air_pressure\': {\'units\': \'mbar\'},\n \'toa_incoming_shortwave_flux\': {\'units\': \'W m^-2\'},\n \'surface_upward_sensible_heat_flux\': {\'units\': \'W m^-2\'},\n \'surface_upward_latent_heat_flux\': {\'units\': \'W m^-2\'},\n \'air_pressure\': {\'units\': \'hPa\'}}\n\nIn [13]: # tendence of total water mixing ratio expected units = g/kg/day                                                                 \n\nIn [14]: # tendence of tendency_of_liquid_ice_static_energy expected units =K/day                                           \n```    \n\n## Configuring SAM to call this function\n\n\nWrite uwnet.sam_interface.call_random_forest \n \nrule sam_run in Snakefile actually runs the SAM model. \n \nparameters as a json file are passed to src.sam.create_case via -p flag.  \n \nExample parameters at assets/parameters_sam_neural_network.json.  \n \nparameters[\'python\'] configures which python function is called. \n',
    'author': 'Noah D. Brenowitz',
    'author_email': 'nbren12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nbren12/uwnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
