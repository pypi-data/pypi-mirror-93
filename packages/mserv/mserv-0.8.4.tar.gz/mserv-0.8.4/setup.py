# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mserv']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.0,<3.0.0',
 'rich>=9.8.0,<10.0.0']

entry_points = \
{'console_scripts': ['mserv = mserv.mserv:mserv_cli']}

setup_kwargs = {
    'name': 'mserv',
    'version': '0.8.4',
    'description': 'A simple wrapper for managing your Minecraft servers.',
    'long_description': "# mserv\nA simple wrapper for managing your Minecraft servers.\n\n## What is it?\nMserv is a little commandline utility I wrote in Python to help me better\nmanage my, and my friends' Minecraft servers.  \n\nMojang offers a DIY *server.jar* file \nwhich you can execute and host a server on your own PC for free. But, what if I wanted\nseparate servers? What if I don't care to go to the Minecraft website and download the file myself?\nOr, what if I don't care to remember the server execution parameters?  \n\nMserv serves to simplify many of these processes, and should make efforts to help those less tech-savvy.\n\n## What can it do?\nThis is a wrapper around the official server.jar from Mojang\nAs of right now, it can...\n\n- Download and generate files from the official server executable\n- Start and shutdown the server\n- Displays network connection information (public ip, port number) so others can join your server\n- Can update the server executable (This is still in testing)\n- Update itself (just run ```pip install --upgrade mserv```)\n\n## What can it NOT do?\nThis script can not:\n- Port forward for you (You have to do that yourself)\n- Execute multiple servers at the same time\n\n# Requirements\n1. Java\n2. Python version 3.8 or above\n\n# Installation\n\n1. EASY - Use Python's package manager pip:\n  ```shell\n  pip install mserv\n  ```\n\nor  \n\n2. TRICKY - Clone this repository:\n```shell\ngit clone https://github.com/mexiquin/mserv.git\n```  \n\nThen execute mserv.py located in the *mserv* directory\n```shell\npython3 ./mserv/mserv/mserv.py\n```\n\n# Generated Help Page\n```\nUsage: mserv.py [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  run\n  setup   Create a new server.\n  update  Download a fresh server.jar file from Mojang.\n\n```\n\n",
    'author': 'Quinton Jasper',
    'author_email': 'dropatuningmetal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mexiquin/mserv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
