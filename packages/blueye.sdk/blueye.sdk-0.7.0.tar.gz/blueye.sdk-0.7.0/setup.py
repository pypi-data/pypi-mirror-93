# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blueye', 'blueye.sdk']

package_data = \
{'': ['*']}

install_requires = \
['blueye.protocol>=1.2.2,<2.0.0',
 'packaging>=20.1,<21.0',
 'requests>=2.22.0,<3.0.0',
 'tabulate>=0.8.5,<0.9.0']

extras_require = \
{'examples': ['asciimatics>=1.11.0,<2.0.0',
              'inputs>=0.5,<0.6',
              'pandas>=0.25.2,<0.26.0',
              'matplotlib>=3.1.1,<4.0.0',
              'webdavclient3>=0.12,<0.13']}

setup_kwargs = {
    'name': 'blueye.sdk',
    'version': '0.7.0',
    'description': 'SDK for controlling a Blueye underwater drone',
    'long_description': '# blueye.sdk\n[![Tests](https://github.com/BluEye-Robotics/blueye.sdk/workflows/Tests/badge.svg)](https://github.com/BluEye-Robotics/blueye.sdk/actions)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BluEye-Robotics/blueye.sdk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BluEye-Robotics/blueye.sdk/context:python)\n[![codecov](https://codecov.io/gh/BluEye-Robotics/blueye.sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/BluEye-Robotics/blueye.sdk)\n[![PyPi-version](https://img.shields.io/pypi/v/blueye.sdk.svg?maxAge=3600)](https://pypi.org/project/blueye.sdk/)\n[![python-versions](https://img.shields.io/pypi/pyversions/blueye.sdk.svg?longCache=True)](https://pypi.org/project/blueye.sdk/)\n_________________\n\n[Read Latest Documentation](https://blueye-robotics.github.io/blueye.sdk/) - [Browse GitHub Code Repository](https://github.com/BluEye-Robotics/blueye.sdk)\n_________________\n\n**Note: This is a pre-release -- Please report any issues you might encounter**\n_________________\nA Python package for remote control of the Blueye Pioneer and Blueye Pro underwater drones.\n\n\n![SDK demo](https://user-images.githubusercontent.com/8504604/66751230-d05c7e00-ee8e-11e9-91cb-d46b433aafa5.gif)\n\n## About Blueye Underwater Drones\nThe Blueye Pioneer and Blueye Pro are underwater drones designed for inspections. It is produced and sold by the Norwegian company [`Blueye Robotics`](https://www.blueyerobotics.com/).\nHere is a Youtube video  that gives a overview of the system and its specifications.\n\n[![about the Blueye Pro video](https://user-images.githubusercontent.com/8504604/94681437-bd52f000-0323-11eb-8cb3-e87c6711cc04.jpg)](https://www.youtube.com/watch?v=HI2CQbnCsoU)\n\n## This SDK and the Blueye drones\nA Blueye drone is normally controlled via a mobile device through the Blueye App ([iOS](https://apps.apple.com/no/app/blueye/id1369714041)/[Android](https://play.google.com/store/apps/details?id=no.blueye.blueyeapp)). The mobile device\nis connected via Wi-Fi to a surface unit, and the Pioneer or Pro is connected to the surface unit via a tether cable.\n\nThis python SDK exposes the functionality of the Blueye app through a Python object. The SDK enables remote control of the Blueye Pioneer and Blueye Pro as well as reading telemetry data and viewing video streams. It is not meant for executing code on the Pioneer.\nTo control the drone you connect your laptop to the surface unit Wi-Fi and run code that interfaces with the Blueye Pro or Blueye Pioneer through the Pioneer Python object.\n\n\nCheck out the [`Quick Start Guide`](https://blueye-robotics.github.io/blueye.sdk/docs/quick_start/) to get started with using the SDK.\n',
    'author': 'Sindre Hansen',
    'author_email': 'sindre.hansen@blueye.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.blueyerobotics.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
