# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leaf']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'simpy>=4.0.0,<5.0.0',
 'tqdm>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'leafsim',
    'version': '0.1.1',
    'description': 'A simulator for Large Energy-Aware Fog computing environments.',
    'long_description': '# LEAF [![PyPI version fury.io](https://badge.fury.io/py/leafsim.svg)](https://pypi.org/project/leafsim/) [![Supported versions](https://img.shields.io/pypi/pyversions/leafsim.svg)](https://pypi.org/project/leafsim/) [![License](https://img.shields.io/pypi/l/leafsim.svg)](https://pypi.org/project/leafsim/)\n\nA simulator for **L**arge **E**nergy-**A**ware **F**og computing environments.\nLEAF enables energy consumption modeling of distributed, heterogeneous, and resource-constrained infrastructure that executes complex application graphs.\n\nFeatures include:\n\n- **Power modeling**: Model the power usage of individual compute nodes, network traffic and applications\n- **Energy-aware algorithms**: Implement dynamically adapting task placement strategies, routing policies, and other energy-saving mechanisms\n- **Dynamic networks**: Nodes can be mobile and can join or leave the network during the simulation\n- **Scalability**: Simulate thousands of devices and applications in magnitudes faster than real time\n- **Exporting**: Export power usage characteristics and other results as CSV files for further analysis\n\n<p align="center">\n  <img src="/images/infrastructure.png">\n</p>\n\n\n## Under Development\n\nThis Python implementation was ported from the [original Java protoype](https://www.github.com/birnbaum/leaf).\nAll future development will take place in this repository.\nHowever, the code is currently under early development and only comes with a minimal working example you can find under `examples/simple`.\n\nFurther examples, including the smart city traffic scenario implemented in the Java prototype will follow soon.\n\n\n## Development\n\n### Build and Publish\n\n> poetry build --format sdist\n> poetry publish\n\n\n## Publications\n\nThe paper behind LEAF is currently under review:\n- Philipp Wiesner and Lauritz Thamsen. "LEAF: Simulating Large Energy-Aware Fog Computing Environments" [under review]\n',
    'author': 'Philipp Wiesner',
    'author_email': 'wiesner@tu-berlin.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dos-group/leaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
