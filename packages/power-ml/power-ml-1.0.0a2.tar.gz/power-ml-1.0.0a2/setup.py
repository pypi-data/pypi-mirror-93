# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['power_ml',
 'power_ml.ai',
 'power_ml.ai.predictor',
 'power_ml.ai.selection',
 'power_ml.data',
 'power_ml.platform',
 'power_ml.stats',
 'power_ml.util']

package_data = \
{'': ['*']}

install_requires = \
['combu>=1.2.1,<2.0.0',
 'joblib>=1.0.0,<2.0.0',
 'numpy>=1.0.0,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'tinydb>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'power-ml',
    'version': '1.0.0a2',
    'description': 'Empowerment Python Machine Learing Stack.',
    'long_description': '# power-ml\n\nEmpowerment Python Machine Learing Stack.\n\n## Install\n\n* Requirements\n   * Poetry\n   * pyenv\n\n```sh\npoetry install --no-dev\n```\n\n## Other Requirements\n\n* lightgbm\n   * For LightGBM model.\n* boto3\n   * For AWS support.\n```\n\n## Development\n\n```sh\n# Setup\npoetry install\n\n# Run lint and test.\nbash scripts/report.bash\n```\n',
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takelushi/power-ml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
