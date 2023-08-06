# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeddfs']

package_data = \
{'': ['*']}

install_requires = \
['natsort>=7', 'pandas>=1.2,<2.0']

extras_require = \
{'hdf5': ['tables>=3.6,<4.0']}

setup_kwargs = {
    'name': 'typeddfs',
    'version': '0.5.0',
    'description': 'Pandas DataFrame subclasses that enforce structure and can self-organize.',
    'long_description': '# Typed DataFrames\n\n[![Version status](https://img.shields.io/pypi/status/typeddfs?label=status)](https://pypi.org/project/typeddfs)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/typeddfs?label=Python)](https://pypi.org/project/typeddfs)\n[![Version on Github](https://img.shields.io/github/v/release/dmyersturnbull/typed-dfs?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/typed-dfs/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/typeddfs?label=PyPi)](https://pypi.org/project/typeddfs)\n[![Build (Actions)](https://img.shields.io/github/workflow/status/dmyersturnbull/typed-dfs/Build%20&%20test?label=Tests)](https://github.com/dmyersturnbull/typed-dfs/actions)\n[![Documentation status](https://readthedocs.org/projects/typed-dfs/badge)](https://typed-dfs.readthedocs.io/en/stable/)\n[![Coverage (coveralls)](https://coveralls.io/repos/github/dmyersturnbull/typed-dfs/badge.svg?branch=main&service=github)](https://coveralls.io/github/dmyersturnbull/typed-dfs?branch=main)\n[![Maintainability](https://api.codeclimate.com/v1/badges/6b804351b6ba5e7694af/maintainability)](https://codeclimate.com/github/dmyersturnbull/typed-dfs/maintainability)\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dmyersturnbull/typed-dfs/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/dmyersturnbull/typed-dfs/?branch=main)  \n[![Created with Tyrannosaurus](https://img.shields.io/badge/Created_with-Tyrannosaurus-0000ff.svg)](https://github.com/dmyersturnbull/tyrannosaurus)\n\n\nPandas DataFrame subclasses that enforce structure and can self-organize.\nBecause your functions can’t exactly accept _any_  DataFrame.\n\nThe subclassed DataFrames can have required and/or optional columns and indices,\nand support custom requirements.\nColumns are automatically turned into indices,\nwhich means **`read_csv` and `to_csv` are always inverses**.\n`MyDf.read_csv(mydf.to_csv())` is just `mydf`.\n\nThe DataFrames will display nicely in Jupyter notebooks,\nand a few convenience methods are added, such as `sort_natural` and `drop_cols`.\n**[See the docs](https://typed-dfs.readthedocs.io/en/stable/)** for more information.\n\n`pip install typeddfs[hdf5]` to install.\n\nPlease note that HDF5 via pytables is \n[unsupported in Python 3.9 on Windows](https://github.com/PyTables/PyTables/issues/854)\nas of 2021-02-03.\n\nSimple example for a CSV like this:\n\n| key   | value  | note |\n| ----- | ------ | ---- |\n| abc   | 123    | ?    |\n\n```python\nfrom typeddfs import TypedDfs\n\n# Build me a Key-Value-Note class!\nKeyValue = (\n    TypedDfs.typed("KeyValue")        # typed means enforced requirements\n    .require("key", dtype=str, index=True)  # automagically make this an index\n    .require("value")                 # required\n    .reserve("note")                  # permitted but not required\n    .strict()                         # don’t allow other columns\n).build()\n\n# This will self-organize and use "key" as the index:\ndf = KeyValue.read_csv("example.csv")\n\n# For fun, let"s write it and read it back:\ndf.to_csv("remke.csv")\ndf = KeyValue("remake.csv")\nprint(df.index_names(), df.column_names())  # ["key"], ["value", "note"]\n\n# And now, we can type a function to require a KeyValue,\n# and let it raise an `InvalidDfError` (here, a `MissingColumnError`):\ndef my_special_function(df: KeyValue) -> float:\n    return KeyValue(df)["value"].sum()\n```\n\nAll of the normal DataFrame methods are available.\nUse `.untyped()` or `.vanilla()` to make a detyped copy that doesn’t enforce requirements.\n\nA small note of caution: [natsort](https://github.com/SethMMorton/natsort) is no longer pinned\nto a specific major version as of version 0.5 because it receives somewhat frequent major updates.\nThis means that the result of typed-df’s `sort_natural` could change.\nYou can pin natsort to a specific major version; e.g. `natsort = "^7"` with [Poetry](https://python-poetry.org/).\n\nTyped-Dfs is licensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n[New issues](https://github.com/dmyersturnbull/typed-dfs/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/typed-dfs/blob/main/CONTRIBUTING.md).  \nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'dmyersturnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/typed-dfs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
