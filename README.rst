battlenet
========================

.. image:: https://pypip.in/v/battlenet/badge.png
   :target: https://crate.io/packages/battlenet

.. image:: https://pypip.in/d/battlenet/badge.png
   :target: https://crate.io/packages/battlenet

.. image:: https://landscape.io/github/vishnevskiy/battlenet/master/landscape.svg
   :target: https://landscape.io/github/vishnevskiy/battlenet/master
   :alt: Code Health

.. image:: https://secure.travis-ci.org/vishnevskiy/battlenet.png?branch=master
   :target: http://travis-ci.org/vishnevskiy/battlenet
   :alt: travis-ci for master branch

.. image:: https://codecov.io/github/vishnevskiy/battlenet/coverage.svg?branch=master
   :target: https://codecov.io/github/vishnevskiy/battlenet?branch=master
   :alt: coverage report for master branch

.. image:: http://www.repostatus.org/badges/0.1.0/active.svg
   :alt: Project Status: Active - The project has reached a stable, usable state and is being actively developed.
   :target: http://www.repostatus.org/#active

Python Library for Blizzard's Community Platform API

Major features
----------------------

* Pythonic

* Unicode normalization

* Lazyloading and eagerloading

* Support locales (en, fr, de, ...)

Requirements
------------

* Python __2.7__. Versions 0.3.3 and prior were compatiable back to python 2.6 (or possibly 2.5). Python3 support is in the works.
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv. If you really want to install
system-wide, you can (using sudo).

.. code-block:: bash

    pip install battlenet

Usage
-----

Making a connection
~~~~~~~~~~~~~~~~~~~~

Global connection settings can be setup so that objects can make connections implicitly.

::

    from battlenet import Connection

    Connection.setup(public_key='your public key', private_key='your private key', locale='fr')

You can also create connections explicitly.

::

    from battlenet import Connection

    connection = Connection(public_key='your public key', private_key='your private key', locale='fr')

Fetching a specific realm
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from battlenet import Realm

    # If a global connection was setup
    realm = Realm(battlenet.UNITED_STATES, 'Nazjatar')

    # Using a specific connection
    realm = connection.get_realm(battlenet.UNITED_STATES, 'Nazjatar')

    print realm.name
    # => Nazjatar

    print realm.is_online()
    # => true

    print realm.type
    # => PVP


Fetching all realms
~~~~~~~~~~~~~~~~~~~~

::

    for realm in connection.get_all_realms(battlenet.UNITED_STATES):
        print realm

Fetching a character
~~~~~~~~~~~~~~~~~~~~~

::

    from battlenet import Character

    # If a global connection was setup
    character = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.GUILD])

    # Using a specific connection
    character = connection.get_character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.GUILD])

    print character.name
    # => Vishnevskiy

    print character.guild.name
    # => Excellence


Fetching a guild
~~~~~~~~~~~~~~~~~

::

    from battlenet import Guild

    # If a global connection was setup
    guild = Guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

    # Using a specific connection
    guild = connection.get_guild(battlenet.UNITED_STATES, 'Nazjatar', 'Excellence')

    print guild.name
    # => Excellence

    leader = guild.get_leader()
    print leader.name
    # => Clí

More Examples
~~~~~~~~~~~~~~~

Read the unit tests inside the tests directory.

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub Issue Tracker <https://github.com/vishnevskiy/battlenet/issues>`_. Pull requests are
welcome. Issues that don't have an accompanying pull request will be worked on
as my time and priority allows.

Development
===========

To install for development:

1. Fork the `battlenet <https://github.com/vishnevskiy/battlenet>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ virtualenv battlenet
    $ cd battlenet && source bin/activate
    $ pip install -e git+git@github.com:YOURNAME/battlenet.git@BRANCHNAME#egg=battlenet
    $ cd src/battlenet

The git clone you're now in will probably be checked out to a specific commit,
so you may want to ``git checkout BRANCHNAME``.

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <http://tox.testrun.org/>`_.

* testing is as simple as:

  * ``pip install tox``
  * ``tox``

* If you want to see code coverage: ``tox -e cov``

  * this produces two coverage reports - a summary on STDOUT and a full report in the ``htmlcov/`` directory

* If you want to pass additional arguments to pytest, add them to the tox command line after "--". i.e., for verbose pytext output on py27 tests: ``tox -e py27 -- -v``

* All tests that actually hit the BattleNet API should be decorated with the ``@pytest.mark.integration`` decorator. This allows us to run these iff the unit tests passed.

Release Checklist
-----------------

1. Open an issue for the release; cut a branch off master for that issue.
2. Confirm that there are CHANGES.rst entries for all major changes.
3. Ensure that Travis tests passing in all environments.
4. Ensure that test coverage is no less than the last release (ideally, 100%).
5. Increment the version number in battlenet/version.py and add version and release date to CHANGES.rst, then push to GitHub.
6. Confirm that README.rst renders correctly on GitHub.
7. Upload package to testpypi, confirm that README.rst renders correctly.

   * Make sure your ~/.pypirc file is correct
   * ``python setup.py register -r https://testpypi.python.org/pypi``
   * ``python setup.py sdist upload -r https://testpypi.python.org/pypi``
   * Check that the README renders at https://testpypi.python.org/pypi/battlenet

8. Create a pull request for the release to be merge into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -a vX.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin vX.Y.Z``

11. Upload package to live pypi:

    * ``python setup.py sdist upload``

10. make sure any GH issues fixed in the release were closed.
