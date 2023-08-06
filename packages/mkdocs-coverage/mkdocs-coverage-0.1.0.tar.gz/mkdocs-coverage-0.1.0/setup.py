# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_coverage']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mkdocs-coverage = mkdocs_coverage.cli:main']}

setup_kwargs = {
    'name': 'mkdocs-coverage',
    'version': '0.1.0',
    'description': 'MkDocs plugin to integrate your coverage HTML report into your site.',
    'long_description': '# MkDocs Coverage Plugin\n\n[![ci](https://github.com/pawamoy/mkdocs-coverage/workflows/ci/badge.svg)](https://github.com/pawamoy/mkdocs-coverage/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/mkdocs-coverage/)\n[![pypi version](https://img.shields.io/pypi/v/mkdocs-coverage.svg)](https://pypi.org/project/mkdocs-coverage/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocs-coverage/community)\n\nMkDocs plugin to integrate your coverage HTML report into your site.\n\n## Requirements\n\nMkDocs Coverage Plugin requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install mkdocs-coverage\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 mkdocs-coverage\n```\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/mkdocs-coverage',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
