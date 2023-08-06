# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_coverage']

package_data = \
{'': ['*']}

entry_points = \
{'mkdocs.plugins': ['coverage = mkdocs_coverage.plugin:MkDocsCoveragePlugin']}

setup_kwargs = {
    'name': 'mkdocs-coverage',
    'version': '0.2.1',
    'description': 'MkDocs plugin to integrate your coverage HTML report into your site.',
    'long_description': '# MkDocs Coverage Plugin\n\n[![ci](https://github.com/pawamoy/mkdocs-coverage/workflows/ci/badge.svg)](https://github.com/pawamoy/mkdocs-coverage/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/mkdocs-coverage/)\n[![pypi version](https://img.shields.io/pypi/v/mkdocs-coverage.svg)](https://pypi.org/project/mkdocs-coverage/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocs-coverage/community)\n\nMkDocs plugin to integrate your coverage HTML report into your site.\n\n## Requirements\n\nMkDocs Coverage Plugin requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install mkdocs-coverage\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 mkdocs-coverage\n```\n\n## Usage\n\n```yaml\n# mkdocs.yml\n\nnav:\n- Coverage report: coverage.md\n\nplugins:\n- coverage:\n    page_name: coverage  # default\n    html_report_dir: htmlcov  # default\n```\n\nNow serve your documentation,\nand go to http://localhost:8000/coverage/\nto see your coverage report!\n\n![coverage index](https://user-images.githubusercontent.com/3999221/106802970-f4376a80-6663-11eb-8665-e9e09f0f4ac0.png)\n![coverage module](https://user-images.githubusercontent.com/3999221/106803017-fe596900-6663-11eb-9df9-973755c5b63e.png)\n',
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
