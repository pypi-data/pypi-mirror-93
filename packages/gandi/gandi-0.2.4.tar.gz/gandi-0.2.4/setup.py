# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gandi', 'gandi.commands']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gandi = gandi.console:run']}

setup_kwargs = {
    'name': 'gandi',
    'version': '0.2.4',
    'description': 'Command line interface to the Gandi API',
    'long_description': 'Gandi CLI Tool\n==============\n\nCommand line interface to the [Gandi API][].\n\n[Gandi API]: https://docs.gandi.net/en/domain_names/advanced_users/api.html\n\nInstallation\n------------\n\n### pip\n\nInstall using pip:\n\n    pip3 install --user gandi\n\n### pipx\n\nInstall using [pipx](https://pipxproject.github.io/pipx/):\n\n    pipx install gandi\n\nConfiguration\n-------------\n\nRun `gandi setup` to create a configuration file at\n`$XDG_CONFIG_HOME/gandi/config`. This will ask for your Gandi API key as well\nas an (optional) default domain name and an (optional) default mailbox ID.\n\nIf you specify a domain name and mailbox ID, subcommands that require these\nparameters will use the values supplied in your config file instead of\nrequiring them as commandline flags.\n\nParameters can also be specified using environment variables, e.g.:\n\n    GANDI_API_KEY=... gandi mbox -d DOMAIN --list\n\nUsage\n-----\n\n    gandi SUBCOMMAND OPTIONS\n\n### Subcommands\n\n**setup**: Setup the Gandi CLI config file\n\n    gandi setup\n\n**alias**: Manage email aliases\n\n    gandi alias [-d DOMAIN] [-m MAILBOXID] (--list | --add ALIAS | --remove ALIAS)\n\nList existing email aliases:\n\n    gandi alias -l\n\nAdd a new alias:\n\n    gandi alias -a ALIAS\n\nRemove an alias:\n\n    gandi alias -r ALIAS\n\n**mbox**: Manage email mailboxes\n\n    gandi mbox [-d DOMAIN] --list\n',
    'author': 'Greg Anders',
    'author_email': 'greg@gpanders.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~gpanders/gandi-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
