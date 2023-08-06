.. image:: https://img.shields.io/pypi/v/jaraco.translate.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.translate.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.translate

.. image:: https://github.com/jaraco/jaraco.translate/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.translate/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

Natural language translation support using Google APIs.


pmxbot plugin
-------------

jaraco.translate supplies a plugin for `pmxbot
<https://github.com/yougov/pmxbot>`_.

To enable, simply install this package alongside pmxbot and
add your Google API key to the pmxbot config::

    Google API key: AB2x...

and then `!translate` away.
