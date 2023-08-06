# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twod']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'twod',
    'version': '0.2.6',
    'description': 'A two-dimensional geometry library for humans.',
    'long_description': '<!-- 2d two-dimension vector point geometry humans -->\n# twod - A Two-Dimensional Geometry Libray for Humans™\n![version][pypi-version]\n![dependencies][dependencies]\n![pytest][pytest-action]\n![license][license]\n![monthly-downloads][monthly-downloads]\n![Code style: black][code-style-black]\n\n[twod][0] "two dee" is a geometry library that supplies\nsimple two-dimensional geometric primtives:\n\n- `twod.Point`\n- `twod.Rect`\n\n## Install\n\nInstalling `twod` is a snap!\n\n```console\n$ python3 -m pip install -U twod\n```\n\n## Development Workflow\n\n```console\n$ git clone https://github.com/JnyJny/twod.git\n$ cd twod\n$ poetry shell\n...\n(twod-...) $ \n```\n\n## Usage Exmaples\n\n```python\n\nfrom twod import Point\n\no = Point()\nb = Point.from_polar(10, 0)\nassert b.distance(o) == 10.0\n```\n\n<!-- end links -->\n[0]: https://github.com/JnyJny/twod.git\n\n<!-- badges -->\n[pytest-action]: https://github.com/JnyJny/twod/workflows/pytest/badge.svg\n[code-style-black]: https://img.shields.io/badge/code%20style-black-000000.svg\n[pypi-version]: https://img.shields.io/pypi/v/twod\n[license]: https://img.shields.io/pypi/l/twod\n[dependencies]: https://img.shields.io/librariesio/github/JnyJny/twod\n[monthly-downloads]: https://img.shields.io/pypi/dm/twod\n',
    'author': 'jnyjny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/twod.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
