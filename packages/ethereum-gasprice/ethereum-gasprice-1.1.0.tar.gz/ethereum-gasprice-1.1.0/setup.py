# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereum_gasprice',
 'ethereum_gasprice.async_wrapper',
 'ethereum_gasprice.async_wrapper.providers',
 'ethereum_gasprice.providers']

package_data = \
{'': ['*']}

install_requires = \
['eth-utils>=1.0.0', 'requests>=2.18.0', 'web3>=5.1.0']

extras_require = \
{'aiohttp': ['aiohttp>=3.5.0']}

setup_kwargs = {
    'name': 'ethereum-gasprice',
    'version': '1.1.0',
    'description': 'Tool for fetching actual gasprice in ethereum blockchain',
    'long_description': 'Ethereum gasprice: Actual gasprice for ethereum blockchain\n=======================================\n\n[![PyPI](https://img.shields.io/pypi/v/ethereum-gasprice)](https://pypi.org/project/ethereum-gasprice/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dw/ethereum-gasprice)](https://pypi.org/project/ethereum-gasprice/)\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FElastoo-Team%2Fethereum-gasprice-py%2Fbadge&style=flat)](https://actions-badge.atrox.dev/Elastoo-Team/ethereum-gasprice-py/goto)\n\nLibrary for fetching actual ethereum blockchain gasprice from different sources:\n[Etherscan Gas Tracker](https://etherscan.io/gastracker), [Eth Gas Station](https://ethgasstation.info/),\n[Etherchain Gasprice Oracle](https://www.etherchain.org/tools/gasPriceOracle),\n[Web3 RPC Method](https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.gasPrice).\n\nRead more about gas and fee from [this article](https://ethereum.org/en/developers/docs/gas/)\n\n# Installation\n\n```bash\npoetry add ethereum-gasprice\n```\n\nor\n\n```bash\npip3 install ethereum-gasprice\n```\n\n# Quickstart\n\n```python\nfrom ethereum_gasprice import GaspriceController, GaspriceStrategy, EthereumUnit\n\nETHERSCAN_API_KEY = "..."\n\n# Pass api key to GaspriceController to initialize provider\ncontroller = GaspriceController(\n    etherscan_api_key=ETHERSCAN_API_KEY,\n    return_unit=EthereumUnit.WEI,\n)\n\n# Get gasprice by one of these strategies:\n# GaspriceStrategy.SLOW, GaspriceStrategy.REGULAR, GaspriceStrategy.FAST, GaspriceStrategy.FASTEST\nactual_gasprice = controller.get_gasprice_by_strategy(GaspriceStrategy.FAST)  # output: 69000000000\n\n# Get all gasprice straregies from first available source:\nactual_gasprices = controller.get_gasprices()  # output: {\'slow\': 10, \'regular\': 15, \'fast\': 20, \'fastest\': 21}\n```\n\n# Documentation\n\nTBD\n\n# License\n\nEthereum gasprice is licensed under the terms of the MIT License (see the file LICENSE).\n',
    'author': 'Nikita Yugov',
    'author_email': 'nikitosnikn@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Elastoo-Team/ethereum-gasprice-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
