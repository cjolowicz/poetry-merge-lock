poetry-merge-lock
=================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

This is a tool for resolving merge conflicts in the lock file of `Poetry`_,
a packaging and dependency manager for Python.
If the merge conflicts cannot be resolved by this tool,
you can use the :option:`--print-content-hash` option to
compute the content hash for the ``metadata.content-hash`` entry,
and resolve the conflicts manually.

.. _Poetry: http://python-poetry.org/


Installation
------------

To install poetry-merge-lock,
run this command in your terminal:

.. code-block:: console

   $ pip install poetry-merge-lock


Usage
-----

poetry-merge-lock's usage looks like:

.. code-block:: console

   $ poetry-merge-lock [OPTIONS]

.. option:: --print-content-hash

   Print the content hash (``metadata.content-hash``).

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.
