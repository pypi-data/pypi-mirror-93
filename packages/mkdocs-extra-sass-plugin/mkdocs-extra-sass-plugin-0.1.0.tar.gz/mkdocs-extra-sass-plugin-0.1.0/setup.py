# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_extra_sass_plugin']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.6.3', 'libsass>=0.15', 'mkdocs>=1.1']

entry_points = \
{'mkdocs.plugins': ['extra-sass = '
                    'mkdocs_extra_sass_plugin.plugin:ExtraSassPlugin']}

setup_kwargs = {
    'name': 'mkdocs-extra-sass-plugin',
    'version': '0.1.0',
    'description': 'This plugin adds stylesheets to your mkdocs site from `Sass`/`SCSS`.',
    'long_description': "# mkdocs-extra-sass-plugin\n\n[![PyPI version](https://img.shields.io/pypi/v/mkdocs-extra-sass-plugin.svg)](https://pypi.org/project/mkdocs-extra-sass-plugin)\n[![PyPI downloads](https://img.shields.io/pypi/dm/mkdocs-extra-sass-plugin.svg)](https://pypi.org/project/mkdocs-extra-sass-plugin)\n\n---\n\nThis plugin adds stylesheets to your mkdocs site from `Sass`/`SCSS`.\n\n## Features\n\n* using [LibSass][LibSass] with [libsass-python][libsass-python].\n\n## How to use\n\n### Installation\n\n1. Install the package with pip:\n\n    ```sh\n    pip install mkdocs-extra-sass-plugin\n    ```\n\n2. Enable the plugin in your `mkdocs.yml`:\n\n    ```yml\n    plugins:\n      - extra-sass\n    ```\n\n    > **Note**: If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.\n\n3. Create a `extra_sass` directory in your working directory _(usually the same directory as` mkdocs.yml`)_, and create **entry point file** named `style.css.sass` or `style.css.scss`.\n\n    ```none\n    (top)\n    ├── docs\n    ：  ...snip...\n    │\xa0\xa0 └── index.md\n    ├── extra_sass\n    ：  ...snip...\n    │\xa0\xa0 └── style.css.scss (or style.css.sass)  # compiler entry point file.\n    └── mkdocs.yml\n    ```\n\nMore information about plugins in the [MkDocs documentation][mkdocs-plugins].\n\n## Contributing\n\nFrom reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].\nIf you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].\n\n[LibSass]: https://sass-lang.com/libsass\n[libsass-python]: https://github.com/sass/libsass-python\n[mkdocs-plugins]: https://www.mkdocs.org/user-guide/plugins/\n[github-issues]: https://github.com/orzih/mkdocs-extra-sass-plugin/issues\n[contributing]: https://github.com/orzih/mkdocs-extra-sass-plugin/blob/master/CONTRIBUTING.md\n",
    'author': 'orzih',
    'author_email': 'orzih@mail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orzih/mkdocs-extra-sass-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
