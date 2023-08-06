# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['so_pip',
 'so_pip._cache',
 'so_pip._vendor',
 'so_pip._vendor.find_imports',
 'so_pip._vendor.find_imports_cruft',
 'so_pip.api_clients',
 'so_pip.cli_clients',
 'so_pip.commands',
 'so_pip.infer_packages_needed',
 'so_pip.licenses',
 'so_pip.models',
 'so_pip.parse_code',
 'so_pip.parse_python',
 'so_pip.parse_python.md',
 'so_pip.support_files',
 'so_pip.update_any',
 'so_pip.utils']

package_data = \
{'': ['*'],
 'so_pip': ['templates/*',
            'templates/js/*',
            'templates/lua/*',
            'templates/php/*',
            'templates/python/*',
            'templates/ruby/*'],
 'so_pip._vendor': ['find_imports_cruft/LICENSE/*']}

install_requires = \
['2to3',
 'astroid',
 'beautifulsoup4',
 'black',
 'diskcache',
 'html2text',
 'jinja2',
 'markdown',
 'nbformat',
 'pip-upgrader',
 'pipreqs',
 'pur',
 'py-stackexchange',
 'pyflakes',
 'pypinfo',
 'pypistats',
 'pyrankvote',
 'python-dotenv',
 'pyupgrade',
 'random_names>=0.1.0',
 'requests',
 'slpp-23',
 'stackapi',
 'stdlib-list',
 'toml',
 'vermin',
 'whats-that-code>=0.1.10']

entry_points = \
{'console_scripts': ['so_pip = so_pip.__main__:main']}

setup_kwargs = {
    'name': 'so-pip',
    'version': '0.1.30',
    'description': 'Generate packages from Stackoverflow answers',
    'long_description': 'so_pip\n======\nEveryone copies code from StackOverflow, but no one is formalizing it.\n\nThis will vendorize the source code of question or answer into a folder and\ngenerate the accessory files to make it look like a python package.\n\nThe feature-set overlaps a bit with [cookie cutter, vendorizing libraries and\nstackoverflow search cli\'s](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md).\n\n[![DepShield Badge](https://depshield.sonatype.org/badges/owner/repository/depshield.svg)](https://depshield.github.io)\n\nInstallation\n------------\nRequires Python 3.7+, tested with 3.7, 3.8, 3.9\n```\npip install so_pip\nso_pip vendorize my_name --question=31049648 --output=output\n```\n\nUsing via [dockerhub](https://hub.docker.com/repository/docker/matthewdeanmartin/so_pip)\n```\n# for mac, unix, cmd.exe, powershell\ndocker pull matthewdeanmartin/so_pip\ndocker run --rm -i -v "$PWD/data:/data" matthewdeanmartin/so_pip --help\n```\nIf you use git bash/mingw64/cygwin, see [run.sh](https://github.com/matthewdeanmartin/so_pip/blob/main/docker/run.sh)\nbecause docker needs help doing a volume mount.\n\n\nUsage\n--------------\nConsider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](https://github.com/matthewdeanmartin/so_pip/blob/main/.so_pip.ini) The app will make best efforts if you don\'t.\n```\n# Turn posts into nicely formated packages\n> so_pip vendorize my_name --question=31049648 | --answer=31049648\n> so_pip search --answer=31049648 --tags=python\n\n# Pip-like commands\n> so_pip uninstall | upgrade {package_name}\n> so_pip list | freeze\n```\n\nDocs\n-----\n* [Examples](https://github.com/matthewdeanmartin/so_pip/tree/main/examples)\n* [CLI](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/cli.md)\n* [Code reuse scanarios you see on StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/scenarios.md)\n* [Features](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/features.md)\n* [Security Considerations](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/security.md)\n* [Prior Art](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md) Similar and overlapping tools.\n* [Contributing *answers* to StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/contributing.md) AKA, fixing answers you found.\n* [Attribution Compliance](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/comply_with_cc_sa.md)\n* [Contributing to so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CONTRIBUTING.md)\n* [Code of Conduct for so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CODE_OF_CONDUCT.md)\n',
    'author': 'Matthew Martin',
    'author_email': 'matthewdeanmartin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthewdeanmartin/so_pip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
