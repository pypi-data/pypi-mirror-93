.. image:: https://img.shields.io/pypi/v/jaraco.postgres.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.postgres.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.postgres

.. image:: https://github.com/jaraco/jaraco.postgres/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.postgres/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/jaracopostgres/badge/?version=latest
   :target: https://jaracopostgres.readthedocs.io/en/latest/?badge=latest

Routines and fixtures for launching and managing
`PostgreSQL <https://postgresql.org>`_ instances.

Pytest Plugin
=============

This library includes a pytest plugin. To enable it, simply
include this library in your test requirements.

Then, in your tests, simply add a ``postgresql_instance``
parameter to your functions.

Instance
--------

The ``postgresql_instance`` is a ``jaraco.postgres.PostgresServer``
instance with ``host`` and ``port`` properties.
