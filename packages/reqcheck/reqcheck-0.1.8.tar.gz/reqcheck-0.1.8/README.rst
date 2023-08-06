reqcheck
========

.. image:: https://img.shields.io/pypi/v/reqcheck.svg
    :target: https://pypi.python.org/pypi/reqcheck
    :alt: Latest Version

.. image:: https://travis-ci.org/jaleskovec/reqcheck.svg?branch=master
    :target: https://travis-ci.org/jaleskovec/reqcheck

.. image:: https://coveralls.io/repos/github/jaleskovec/reqcheck/badge.svg
    :target: https://coveralls.io/github/jaleskovec/reqcheck

Compare installed Python package versions with PyPI. Display the current
version, latest version and age for each installed package.

Example output:

::

      Package    Current Version    Latest Version    Behind                             Age
      ---------  -----------------  ----------------  ---------------------------------  -------------------------------
      certifi    2020.12.5          2020.12.5         latest                             ~ 53 days (2020-12-05)
      chardet    3.0.4              4.0.0             -1 version (~ 3 years 186 days)    ~ 3 years 235 days (2017-06-08)
      idna       2.5                3.1               -7 versions (~ 3 years 304 days)   ~ 3 years 328 days (2017-03-07)
      requests   2.17.3             2.25.1            -15 versions (~ 3 years 201 days)  ~ 3 years 244 days (2017-05-29)
      urllib3    1.21.1             1.26.3            -22 versions (~ 3 years 270 days)  ~ 3 years 272 days (2017-05-02)

Installation
------------

To install reqcheck, simply use pip:

::

    $ pip install reqcheck

Usage
-----

You can check requirements directly using stdin:

::

    $ pip freeze | reqcheck

You can check requirements in a virtualenv:

::

    $ reqcheck -v /path/to/venv

You can check requirements on the command line:

::

    $ reqcheck requests==2.10.0 mock==2.0.0

Display usage help:

::

    $ reqcheck --help

Contributing
------------

1. Check the pull requests to ensure that your feature hasn't been
   requested already
2. Fork the repository and make your changes in a separate branch
3. Add unit tests for your changes
4. Submit a pull request
5. Contact the maintainer
