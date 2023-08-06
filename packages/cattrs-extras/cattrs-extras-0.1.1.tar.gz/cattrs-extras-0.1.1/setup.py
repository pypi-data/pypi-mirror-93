# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cattrs_extras', 'cattrs_extras.tortoise']

package_data = \
{'': ['*']}

install_requires = \
['cattrs>=1.0.0,<2.0.0',
 'dateutils>=0.6.12,<0.7.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'typing-inspect>=0.6.0,<0.7.0']

extras_require = \
{'tortoise': ['tortoise-orm>=0.16.20,<0.17.0']}

setup_kwargs = {
    'name': 'cattrs-extras',
    'version': '0.1.1',
    'description': 'Advanced converters for cattrs',
    'long_description': "# cattrs-extras\n\nThis package contains advanced converter classes for [cattrs](https://github.com/Tinche/cattrs), a great serialization library built around [attrs](https://github.com/python-attrs/attrs).\n\n## Key features \n\n* Support for additional types: Decimal, bool, datetime, date, timedelta\n* Alternative structuring algorithm capable of handling complex Unions without registering additional hooks \n* Human-readable exceptions on structuring failure\n* Support for Tortoise ORM models serialization (including relations)\n* Additional class and Tortoise field for reversed enumerations (serialized to member name instead of value)\n\n## Installation\n\n```shell-script\nDEV=0 PYTHON=python make install  # remove PYTHON to use pyenv\nmake build\n```\n\n## Usage\n\n```python\nfrom enum import Enum\nfrom decimal import Decimal\nfrom datetime import datetime\nfrom attr import dataclass\nfrom cattrs_extras.converter import Converter\n\nclass Color(Enum):\n    RED = 'RED'\n    GREEN = 'GREEN'\n\n@dataclass(kw_only=True)\nclass Apple:\n    weight: Decimal\n    color: Color\n    best_before: datetime\n    sweet: bool\n\nconverter = Converter()\nraw_apple = {\n    'weight': '200.5',\n    'color': 'RED',\n    'best_before': '2020-04-02T12:00:00',\n    'sweet': 'true'\n}\n\napple = converter.structure(raw_apple, Apple)\nassert apple == Apple(weight=Decimal('200.5'), color=Color.RED, best_before=datetime(2020, 4, 2, 12, 0), sweet=True)\n\nraw_apple = converter.unstructure(apple)\nassert raw_apple == {'weight': '200.5', 'color': 'RED', 'best_before': 1585818000.0, 'sweet': True}\n```\n\n\n## Tortoise ORM\n\nImportant note: Tortoise ORM have chosen [pydantic](https://github.com/samuelcolvin/pydantic) as a serialization library so better to stick with it. However pydantic support is still WIP, you can check current status [here](https://tortoise-orm.readthedocs.io/en/latest/contrib/pydantic.html).\n\n```python\nfrom cattrs_extras.tortoise.converter import TortoiseConverter\nfrom cattrs_extras.tortoise.model import Model\nfrom tortoise import fields\n\n# TODO: ReversedCharEnumField example\nclass AppleModel(Model):\n    id = fields.IntField(pk=True)\n    weight = fields.DecimalField(20, 10)\n    color = fields.CharEnumField(Color)\n    best_before = fields.DateField()\n    sweet = fields.BooleanField()\n\n# NOTE: Replace with module name of your models\ntortoise_converter = TortoiseConverter('cattrs_extras.tortoise.model')\n\napple_model = tortoise_converter.structure(raw_apple, AppleModel)\nassert apple_model == AppleModel(weight=Decimal('200.5'), color=Color.RED, best_before=datetime(2020, 4, 2, 12, 0), sweet=True)\n\nraw_apple = tortoise_converter.unstructure(apple_model)\nassert raw_apple == {'id': None, 'weight': '200.5', 'color': 'RED', 'best_before': 1585774800.0, 'sweet': True}\n```\n\n## Limitations\n\n* [PEP 563 – Postponed Evaluation of Annotations](https://www.python.org/dev/peps/pep-0563/) is not supported at the moment. Attempt to import `__future__.annotations` in module containing models will lead to exception. However you can still use strings as typehints.\n* Backward relations in Tortoise models are ignored during structuring even if fetched. Not sure if we should fix it.",
    'author': 'Lev Gorodetskiy',
    'author_email': 'github@droserasprout.space',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/droserasprout/cattrs-extras',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
