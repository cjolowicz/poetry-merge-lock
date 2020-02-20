[![Tests](https://github.com/cjolowicz/poetry-merge-lock/workflows/Tests/badge.svg)](https://github.com/cjolowicz/poetry-merge-lock/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/cjolowicz/poetry-merge-lock/branch/master/graph/badge.svg)](https://codecov.io/gh/cjolowicz/poetry-merge-lock)
[![PyPI](https://img.shields.io/pypi/v/poetry-merge-lock.svg)](https://pypi.org/project/poetry-merge-lock/)
[![Read the Docs](https://readthedocs.org/projects/poetry-merge-lock/badge/)](https://poetry-merge-lock.readthedocs.io/)

# poetry-merge-lock

This is a tool for resolving merge conflicts in the lock file of
[Poetry](http://python-poetry.org/),
a packaging and dependency manager for Python.
If the merge conflicts cannot be resolved by this tool,
you can use the `--print-content-hash` option to
compute the content hash for the `metadata.content-hash` entry,
and resolve the conflicts manually.

## Installation

To install poetry-merge-lock,
run this command in your terminal:

```sh
$ pip install poetry-merge-lock
```

## Documentation

[Read the full documentation](https://poetry-merge-lock.readthedocs.io/)
