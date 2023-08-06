v5.1.0
======

#7: Allow ``encoding`` parameter to ``initdb``.

Package now uses PEP 420 for namespace package.

5.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

4.3
===

#6: Avoid use of deperecated ``yield_fixture``.

4.2
===

Refresh package metadata.

4.1
===

Added PostgresDatabase.ensure_user, which will not fail if the
user already exists. In PostgresServer.create, use ensure_user
to allow multiple databases to be created using the same
user.

4.0
===

PostgresDatabase no longer uses 'pmxtest' as the default user,
but instead the username defaults to the database name.

3.0.1
=====

#2: When searching heuristic paths, sort parsed version numbers
numerically so that 10 is greater than 9.

3.0
===

Removed global variables and behavior on import:

- root
- INITDB
- PG_CTL
- PSQL
- POSTGRES

Instead, use ``PostgresFinder.find_root()``.

2.0.1
=====

#1: Fix version detection on Postgres 10.0.

2.0
===

PostgresServer now creates all databases with a default
locale of ``en_US.UTF-8``. Now, databases will be
Unicode-capable by default. To restore the original
behavior, deferring to the system locale, pass
``locale=None`` to ``initdb``.

1.6
===

Add ``.create`` convenience method to PostgresServer.

1.5
===

Project is now released automatically through Travis
Continuous Integration.

Add Trove classifier for Pytest Framework.

1.4
===

Moved hosting to Github and updated skeleton.

1.3
===

Add ``postgresql_instance`` fixture.

1.2
===

Added some logging info to initdb, start, stop.

Substantial improvements for test suite.

1.1
===

Allow the POSTGRESQL_HOME environment variable to stipulate where
the Postgres binaries must be found, overriding heuristic search.

1.0
===

Initial release, using models from yg.test 4.1.
