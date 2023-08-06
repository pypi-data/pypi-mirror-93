# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['boozelib']
extras_require = \
{'dev': ['bump2version>=1.0.0,<2.0.0',
         'pre-commit>=2.3.0,<3.0.0',
         'towncrier>=19.2.0,<20.0.0'],
 'doc': ['sphinx>=3.0.3,<4.0.0'],
 'test': ['nox>=2019.11.9,<2020.0.0']}

setup_kwargs = {
    'name': 'boozelib',
    'version': '0.6.0',
    'description': 'A Python module containing a couple of tools to calculate the blood alcohol content of people.\n',
    'long_description': '# boozelib\n\n**VERSION**: `0.6.0`\n\nA Python module containing a couple of tools to calculate the\n**blood alcohol content** of people.\n\nIt\'s at home at GitHub: <https://github.com/brutus/boozelib/>.\n\n# Install\n\nYou can install it from [PyPi], it is known as `boozelib` and has no\ndependencies:\n\n```shell\npip install --user boozelib\n```\n\n# Usage\n\nThe two main functions are:\n\n-   `get_blood_alcohol_content(age, weight, height, sex, volume, percent)`\n\n    Return the **blood alcohol contents** raise (per mill) for a person after a\n    drink.\n\n    Given a drink containing _volume_ (ml) of _percent_ (vol/vol) alcohol, for a\n    person with _age_ (years), _weight_ (kg) and _height_ (cm) — using a\n    formular for "female body types" if _sex_ is true.\n\n-   `get_blood_alcohol_degradation(age, weight, height, sex, minutes=1)`\n\n    Return the **alcohol degradation** (per mill) for a person over _minutes_.\n\n    For a person with _age_ (years), _weight_ (kg) and _height_ (cm), over the\n    given _minutes_ — using a formular for "female body types" if _sex_ is true.\n\n## Examples\n\n```python\n>>> from boozelib import get_blood_alcohol_content\n\n>>> get_blood_alcohol_content(\n... \tage=32, weight=96, height=186, sex=False, volume=500, percent=4.9\n... )\n0.28773587455687716\n\n>>> get_blood_alcohol_content(\n... \tage=32, weight=48, height=162, sex=True, volume=500, percent=4.9\n... )\n0.5480779730398769\n\n>>> from boozelib import get_blood_alcohol_degradation\n\n>>> get_blood_alcohol_degradation(\n... \tage=32, weight=96, height=186, sex=False, minutes=60\n... )\n0.21139778538872606\n\n>>> get_blood_alcohol_degradation(\n... \tage=32, weight=48, height=162, sex=True, minutes=60\n... )\n0.20133476560648536\n\n```\n\n## Documentation\n\nSee the source or the [documentation] for more information and the used\n[formulas].\n\n# Testing\n\n[nox] is used as a test runner (with [ward] as the framework). So you need\nto have `nox` installed, before you can run the test suit like this:\n\n```shell\nnox\n```\n\nIf you already have the _development environment_ activated (see below), you\ncan skip the install and just run:\n\n```shell\nmake tests\n```\n\nIf something fails, please get in touch.\n\n# Development Setup\n\n[Poetry] is used to manage a _virtual environment_ for the development setup.\n\nA `Makefile` is provided, that collects some common tasks. You have to run\nthe following **once**, to setup your environment:\n\n```shell\nmake setup\n```\n\n# Thanks and Contributions\n\n-   Big hugs to Mathilda for hanging around and helping me figuring out all\n    that math and biology stuff.\n\nIf you find bugs, issues or anything else, please use the [issue tracker] on\nGitHub. Issues and PRs are welcome ❤️\n\n[documentation]: https://boozelib.readthedocs.org/\n[formulas]: https://boozelib.readthedocs.org/en/latest/background.html\n[issue tracker]: https://github.com/brutus/boozelib/issues\n[nox]: https://nox.thea.codes/\n[poetry]: https://python-poetry.org/\n[pypi]: https://pypi.org/project/BoozeLib/\n[ward]: https://wardpy.com/\n',
    'author': 'Brutus',
    'author_email': 'brutus.dmc@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brutus/boozelib/',
    'package_dir': package_dir,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
