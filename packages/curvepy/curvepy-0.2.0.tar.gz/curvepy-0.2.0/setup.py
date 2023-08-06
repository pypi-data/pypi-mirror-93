# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curvepy', 'curvepy.extension']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.12.1,<0.13.0',
 'intervalpy>=0.1.0,<0.2.0',
 'numpy>=1.15.0,<2.0.0',
 'pyduration>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['test = pytest:main']}

setup_kwargs = {
    'name': 'curvepy',
    'version': '0.2.0',
    'description': 'A mathematical and financial function curve utility library.',
    'long_description': '# curvepy\n\n![Tests](https://github.com/diatche/curvepy/workflows/Tests/badge.svg)\n\nA mathematical and financial function curve utility library for Python.\n\n# Installation\n\nWith [poetry](https://python-poetry.org):\n\n```bash\npoetry add curvepy\n```\n\nOr with pip:\n\n```\npip3 install curvepy\n```\n\n# Usage\n\nHave a look at the [documentation](https://diatche.github.io/curvepy/).\n\n## Basic usage:\n\n```python\n# Create a line\nfrom curvepy import Line\n\nline = Line(const=1, slope=2)\nassert line.y(0) == 1\nassert line.y(1) == 3\n\n# Function arithmetic\nline2 = Line(const=-1, slope=-2)\nline_sum = line1 + line2\nassert line_sum.y(0) == 0\nassert line_sum.y(1) == 0\n```\n\n## JSON Format\n\n**Function values:**\n\nFunctions are denoted by `$`, for example, `$add`. Available functions:\n\n- `$add`: Adds values. Example: `{ "$add": [1, 2] }`, which results in `1 + 2`.\n- `$line`: Adds values. Example: `{ "$line": { "points": [[1, 2], [2, 3]] } }` which results in a line joining the points `(1, 2)` and `(2, 3)`.\n\nFor other functions, refer to `Curve` documentation.\n\nDecorators modify applicable values and functions inside of them as well as deeply nested values. Available decorators:\n\n- `@date`: Converts all string values to seconds from Unix epoch. If no GMT offset is given, uses the local time zone at the time of parsing.\n- `@log`: Converts all number literals to log space. On exit from the decorator, the result is raised bacj by the base into linear space. Available varaints: `@log2`, `@log10`.\n- `@args`: Allows using both named and unamed arguments in a function. For example: `{ \'$raised\': { \'@args\': [4], \'base\': 2 } }`, which will result in `pow(2, 4)`.\n\nA full example:\n\nThe following price will be in the form of a line (on a log chart) joining the prices **10080.2** and **8975.0** on dates **8 May 2020 11:01 am** and **13 May 2020 5 am** respectively.\n\n```json\n{\n    "price": {\n        "@log": {\n            "$line": {\n                "points": [\n                    [{"@date": "2020-05-08 11:01"}, 10080.2],\n                    [{"@date": "2020-05-13 05:00"}, 8975.0]\n                ]\n            }\n        }\n    }\n}\n```\n\n# Development\n\n## Setup\n\nClone repository and run:\n\n```bash\npoetry install\n```\n\n## Running Unit Tests\n\n```bash\npoetry run test\n```\n\n## Updating Documentation\n\nThe module [pdoc3](https://pdoc3.github.io/pdoc/) is used to automatically generate documentation. To update the documentation:\n\n1. Install `pdoc3` if needed with `pip3 install pdoc3`.\n2. Navigate to project root and install dependencies: `poetry install`.\n3. Generate documetation files with: `pdoc3 -o docs --html curvepy`.\n4. The new files will be in `docs/curvepy`. Move them to `docs/` and replace existing files.\n\nIf you get errors about missing modules, make sure you have activated the python enviroment (in .venv) and that there are no python version mismatches. If so, use `poetry env use <python version>; poetry install` to fix.\n',
    'author': 'Pavel Diatchenko',
    'author_email': 'diatche@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diatche/func',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)
