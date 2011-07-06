battlenet
=====================

Python Library for Blizzard's Community Platform API

Major features
----------------------

* Pythonic

* Unicode normalization

* Lazyloading and eagerloading

* Eventlet support

Making a connection
----------------------

Global connection settings can be setup so that objects can make connections implicitly.

::

    from battlenet import Connection

    Connection.setup(public_key='your public key', private_key='your private key')

You can also create connections explicitly.

::

    from battlenet import Connection

    connection = Connection(public_key='your public key', private_key='your private key')

Fetching a specific realm
-------------------------

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
-------------------------

::

    for realm in connection.get_all_realms():
        print realm

Fetching a character
----------------------

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
----------------------

::

    from battlenet import Character

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
----------------------

Read the unit tests inside the tests directory.

TODO
----------------------

* Better abstraction over data API
* Documentation
* Python 3 Support
