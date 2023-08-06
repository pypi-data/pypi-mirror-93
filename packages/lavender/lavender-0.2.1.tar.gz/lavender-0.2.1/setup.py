# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lavender', 'lavenderd', 'llib2to3', 'llib2to3.pgen2']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'mypy_extensions>=0.4.3,<0.5.0',
 'pathspec>=0.6.0,<0.9',
 'regex>=2020.1.8',
 'toml>=0.10.1,<0.11.0',
 'typed-ast>=1.4.0,<2.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6,<0.9'],
 'd': ['aiohttp>=3.3.2,<4.0.0', 'aiohttp_cors>=0.7.0,<0.8.0']}

entry_points = \
{'console_scripts': ['lavender = lavender:patched_main',
                     'lavenderd = lavenderd:patched_main[d]']}

setup_kwargs = {
    'name': 'lavender',
    'version': '0.2.1',
    'description': 'The slightly more compromising code formatter.',
    'long_description': '# Lavender\n\n[![PyPI](https://img.shields.io/pypi/v/lavender.svg)](https://pypi.python.org/pypi/lavender)\n\nA slightly more compromising Python code formatter, based on the latest stable release of\n[Black](https://github.com/python/black#readme)\n([`20.8b10`](https://github.com/psf/black/releases/tag/20.8b1) at the time of writing).\n\n## Differences from Black\n\n- The default line length is 99 instead of 88 (configurable with `--line-length`).\n- Single quoted strings are preferred (configurable with\n `--string-normalization none/single/double`).\n- Empty lines between `class`es and `def`s are treated no differently from other code. The old\n  behavior, which sometimes inserts double empty lines between them, remains available via\n  `--special-case-def-empty-lines`.\n- The Vim plugin configuration variable for line length is named `g:lavender_line_length` instead\n  of `g:lavender_linelength`, for consistency with the other configuration variable names.\n\n## Documentation\n\nRead up on [Black](https://github.com/python/black#readme), but replace `black` with `lavender` in your\nhead.\n\n## Development\n\n[Poetry](https://poetry.eustace.io/) is recommended for managing Python development tooling.\n\nTo initialize an isolated Python development environment for Lavender:\n\n```\npoetry install\n```\n\n### Code Formatting\n\nCode formatting for Python is handled by Lavender itself.\n\nTo check that the code is correctly formatted:\n\n```\npoetry run lavender --check .\n```\n\nTo auto-format the code:\n\n```\npoetry run lavender .\n```\n\n### Type Checking\n\nType checking for Python is handled by [mypy](https://github.com/python/mypy#readme).\n\nTo check that the code is correctly typed:\n\n```\npoetry run mypy .\n```\n\n## License\n\nLavender is Copyright (c) 2019-2021 Michael Smith &lt;michael@spinda.net&gt;\n\nBlack, the software on which it was based, is Copyright (c) 2018-2020 Łukasz Langa\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the MIT\nLicense.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without\neven the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the MIT\nLicense for more details.\n\nYou should have received a [copy](LICENSE) of the MIT License along with this program. If not, see\n[http://opensource.org/licenses/MIT](http://opensource.org/licenses/MIT).\n\n### Contribution\n\nUnless you explicitly state otherwise, any contribution intentionally submitted for inclusion in\nthis work by you shall be licensed as above, without any additional terms or conditions.\n\n[modeline]: # ( vim: set tw=99 ts=2 sw=2 et: )\n',
    'author': 'Michael Smith',
    'author_email': 'michael@spinda.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spinda/lavender#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
