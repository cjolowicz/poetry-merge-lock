poetry-merge-lock
=================

.. badges-begin

|Tests| |Codecov| |PyPI| |Python Version| |Read the Docs| |License| |Black| |pre-commit| |Dependabot|

.. |Tests| image:: https://github.com/cjolowicz/poetry-merge-lock/workflows/Tests/badge.svg
   :target: https://github.com/cjolowicz/poetry-merge-lock/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/cjolowicz/poetry-merge-lock/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/cjolowicz/poetry-merge-lock
   :alt: Codecov
.. |PyPI| image:: https://img.shields.io/pypi/v/poetry-merge-lock.svg
   :target: https://pypi.org/project/poetry-merge-lock/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/poetry-merge-lock
   :target: https://pypi.org/project/poetry-merge-lock
   :alt: Python Version
.. |Read the Docs| image:: https://readthedocs.org/projects/poetry-merge-lock/badge/
   :target: https://poetry-merge-lock.readthedocs.io/
   :alt: Read the Docs
.. |License| image:: https://img.shields.io/pypi/l/poetry-merge-lock
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=cjolowicz/poetry-merge-lock
   :target: https://dependabot.com
   :alt: Dependabot

.. badges-end

This is a tool for resolving merge conflicts in the lock file of Poetry_,
a packaging and dependency manager for Python.
If the merge conflicts cannot be resolved by this tool,
you can use the ``--print-content-hash`` option to
compute the content hash for the ``metadata.content-hash`` entry,
and resolve the conflicts manually.

.. _Poetry: http://python-poetry.org/


Installation
------------

To install poetry-merge-lock,
run this command in your terminal:

.. code:: console

   $ pip install poetry-merge-lock


Documentation
-------------

`Read the full documentation`__

__ https://poetry-merge-lock.readthedocs.io/
