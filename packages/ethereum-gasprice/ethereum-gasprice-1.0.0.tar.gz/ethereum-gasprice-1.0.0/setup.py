# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereum_gasprice', 'ethereum_gasprice.providers']

package_data = \
{'': ['*']}

install_requires = \
['eth-utils>=1.10.0,<2.0.0', 'requests>=2.25.1,<3.0.0', 'web3>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'ethereum-gasprice',
    'version': '1.0.0',
    'description': 'Tool for fetching actual gasprice in ethereum blockchain',
    'long_description': 'Ethereum gasprice: Actual gasprice for ethereum blockchain\n=======================================\n\n# Installation\n\nTBD\n\n# Quickstart\n\n```python\nfrom ethereum_gasprice import GaspriceController, GaspriceStrategy\n\nETHERSCAN_API_KEY = "..."\n\ncontroller = GaspriceController(etherscan_api_key=ETHERSCAN_API_KEY)\nactual_gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)  # output: 69\n```\n\n# Documentation\n\nTBD\n\n\n# License\n\nEthereum gasprice is licensed under the terms of the MIT License (see the file LICENSE).\n',
    'author': 'Nikita Yugov',
    'author_email': 'nikitosnikn@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Elastoo-Team/ethereum-gasprice-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
