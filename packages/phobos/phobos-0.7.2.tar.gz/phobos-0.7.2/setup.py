# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phobos',
 'phobos.augs',
 'phobos.grain',
 'phobos.logger',
 'phobos.loss',
 'phobos.metrics',
 'phobos.runner']

package_data = \
{'': ['*']}

install_requires = \
['MedPy==0.4.0',
 'albumentations==0.5.2',
 'numpy==1.18.1',
 'numpydoc>=1.1.0,<2.0.0',
 'polyaxon-sdk==1.5.4',
 'polyaxon==1.5.4',
 'pytorch_lightning>=0.9.0,<0.10.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'sphinx-issues>=1.2.0,<2.0.0',
 'sphinx-prompt>=1.3.0,<2.0.0',
 'sphinx_rtd_theme>=0.4.3,<0.5.0',
 'torch==1.7.1',
 'torchvision>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'phobos',
    'version': '0.7.2',
    'description': 'Training utility library and config manager for Granular Machine Vision research',
    'long_description': '===================\nPhobos\n===================\n\n\nUtility package for satellite machine learning training\n\n\n* Free software: MIT license\n* Documentation: docs.granular.ai/phobos.\n\nDependencies\n------------\n\n* gsutil\n* kubectl\n* poetry\n* twine\n\nFeatures\n--------\n\n* Polyaxon auto-param capture\n* Configuration enforcement and management for translation into Dione environment\n* Precomposed loss functions and metrics\n\n\nTODO\n----\n\n* Shift build logic from cloudbuild to github actions\n\n\nBuild Details\n-------------\n\n* packages are managed using poetry\n* packages poetry maintains pyproject.toml\n* PRs and commits to `develop` branch trigger a google cloudbuild (image: cloudbuild.yaml, docs: cloudbuild_docs.yaml)\n* Dockerfile builds image by exporting poetry dependencies as tmp_requirements.txt and installing them\n',
    'author': 'Sagar Verma',
    'author_email': 'sagar@granular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/granularai/phobos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
