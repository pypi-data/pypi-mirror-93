# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['power_ml',
 'power_ml.ai',
 'power_ml.ai.predictor',
 'power_ml.data',
 'power_ml.stats',
 'power_ml.util']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.63,<2.0.0',
 'joblib>=1.0.0,<2.0.0',
 'lightgbm>=3.1.1,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'power-ml',
    'version': '1.0.0a0',
    'description': 'Empowerment Python Machine Learing Stack.',
    'long_description': None,
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
