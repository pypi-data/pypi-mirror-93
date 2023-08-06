# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcadminbot', 'mcadminbot.bot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'cysystemd>=1.4.2,<2.0.0',
 'discord.py>=1.3.4,<2.0.0',
 'loguru>=0.5.1,<0.6.0',
 'mctools>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['mcadminbot = mcadminbot.entry:_main']}

setup_kwargs = {
    'name': 'mcadminbot',
    'version': '1.0.0',
    'description': 'A Discord bot used to manage a Minecraft server.',
    'long_description': '# mcadminbot\n\n[![PyPI](https://img.shields.io/pypi/v/mcadminbot?style=plastic)](https://pypi.org/project/mcadminbot/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mcadminbot?style=plastic)](https://pypi.org/project/mcadminbot/)\n\nA Discord bot that allows permitted server members and roles to administrate a Minecraft server over RCON through chat messages.\n\n## Docmentation\n\nVisit the [official documentation](https://mcadminbot.readthedocs.io/en/latest/) for detailed installation and usage instructions.\n\n## Todo\n\n* [ ] Implement more Minecraft commands\n* [ ] Write tests and implement automated testing of branches\n* [x] Implement proper semantic versioning and CI/CD\n\n## Notes\n\n* Any commits or merges into the `master` branch need to follow the [Angular commit message guidelines](https://github.com/conventional-changelog/conventional-changelog/tree/master/packages/conventional-changelog-angular).\n',
    'author': 'Matt Bobke',
    'author_email': 'mcbobke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mcadminbot.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
