===============================
datemore
===============================

.. image:: https://github.com/romnn/datemore/workflows/test/badge.svg
        :target: https://github.com/romnn/datemore/actions
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/datemore.svg
        :target: https://pypi.python.org/pypi/datemore
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnn/datemore
        :target: https://github.com/romnn/datemore
        :alt: License

.. image:: https://codecov.io/gh/romnn/datemore/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnn/datemore
        :alt: Test Coverage

""""""""

This is a small python package that wraps useful extension helper methods
around the standard library ``datetime`` package.

.. code-block:: console

    $ pip install datemore

This package extends ``date`` and ``datetime`` objects with
useful methods for:

- Localizing ``date`` and ``datetime`` objects
- Adding and subtracting
- Generating date ranges
- Mocking (you cannot mock builtins, so why not use this library in the first place :wink:)

Example:

.. code-block:: python

    import datemore.date
    sunday = datemore.date.Date(2020, 2, 2)
    tuesday = sunday.add_days(2)
    passed_days = sunday.range_to(tuesday)
    tuesday.native()  # Get the native datetime.date object

Do you want to add new extensions? Go ahead!
Contributions are welcome, have a look at `CONTRIBUTING <CONTRIBUTING.rst>`_.

Development
-----------

For detailed instructions see `CONTRIBUTING <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
