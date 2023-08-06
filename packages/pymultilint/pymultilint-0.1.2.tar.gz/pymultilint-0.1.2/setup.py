# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['multilint']
install_requires = \
['autoflake==1.4',
 'black==20.8b1',
 'click==7.1.2',
 'invoke>=1.5.0,<2.0.0',
 'isort==5.7.0',
 'jedi==0.17.2',
 'mypy==0.800',
 'parso==0.7.1',
 'pylint>=2.6.0,<3.0.0',
 'toml==0.10.2']

entry_points = \
{'console_scripts': ['gendocs = tasks:gendocs',
                     'multilint = multilint:main',
                     'srvdocs = tasks:srvdocs']}

setup_kwargs = {
    'name': 'pymultilint',
    'version': '0.1.2',
    'description': 'Utility tying multiple code quality tools together',
    'long_description': '# Multilint (for Python)\n\n[![Actions Test Workflow Widget](https://github.com/gkze/multilint/workflows/ci/badge.svg)](https://github.com/gkze/multilint/actions?query=workflow%3Aci)\n[![PyPI Version](https://img.shields.io/pypi/v/pymultilint)](https://pypi.org/project/pymultilint/)\n[![Pdoc Documentation](https://img.shields.io/badge/pdoc-docs-green)](https://gkze.github.io/multilint/multilint.html)\n\nA utility tying together multiple linting and other code quality tools\n\nMultilint allows running several code quality tools under the same interface.\nThis is convenient as it saves time on writing multiple linter / formatter /\nchecker invocations every time in a project.\n\nAdditionally, for tools that do\nnot currently support configuration via `pyproject.toml`\n([PEP-621](https://www.python.org/dev/peps/pep-0621/)), Multilint exposes a\nconfiguration interface for them. This allows for centralized codification of\nconfiguration of all code quality tools being used in a project.\n\nExample relevant sections from a `pyproject.toml`:\n\n```toml\n[tool.autoflake]\nrecursive = true\nin_place = true\nignore_init_module_imports = true\nremove_all_unused_imports = true\nremove_unused_variables = true\nverbose = true\nsrcs = ["."]\n\n[tool.mypy]\nsrc = "."\n\n[tool.multilint]\ntool_order = ["autoflake", "isort", "black", "mypy"]\n```\n\nCurrently, the only supported configuration option for Multilint is\n`tool_order` which defines the execution order of supported tools.\n\nAt the time of writing of this README (2020-01-31), neither\n[Autoflake](https://github.com/myint/autoflake/issues/59) nor\n[Mypy](https://github.com/python/mypy/issues/5205https://github.com/python/mypy/issues/5205)\nsupport configuration via `pyproject.toml`. While support for each may or may\nnot be added at some point in the future, with multilint configuring these tools\nis possible **today**.\n\n## Supported Tools\n\n* [Autoflake](https://github.com/myint/autoflake) - removes unused imports and\n  unused variables as identified by [Pyflakes](https://github.com/PyCQA/pyflakes)\n* [Isort](https://pycqa.github.io/isort/) - sorts imports according to specified\n  orders\n* [Black](https://black.readthedocs.io/en/stable/) - the self-proclaimed\n  "uncompromising code formatter" - formats Python source with an opinionated\n  style\n* [Mypy](http://mypy-lang.org) - static type checker for Python\n* [Pylint](https://www.pylint.org) - general best practices linter\n* [Pydocstyle](http://www.pydocstyle.org/en/stable/) - in-source documentation\n  best practices linter\n\nSupport for more tools may be added by subclassing the\n[`ToolRunner`](multilint.py#L130) class and overriding the\n[`.run(...)`](multilint.py#L162) method.\n\nThere are some utilities provided, such as:\n\n* A logger that masquerades as a TextIO object to allow capturing tool output\n  from within and a configuration\n* A mapping for tool configuration that is automatically available in the\n  `ToolRunner` class (as long as it is registered in the\n  [`Tool`](multilint.py#L47)) enum, the [`TOOL_RUNNERS`](multilint.py#L440)\n  mapping, and declared in the [`DEFAULT_TOOL_ORDER`](multilint.py#L459) class\n  variable of `Multilint`.\n\nDocumentation about adding support for more tools to Multilint may be added in\nthe future.\n',
    'author': 'George Kontridze',
    'author_email': 'george.kontridze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkze/multilint',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
