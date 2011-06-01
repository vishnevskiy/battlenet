battlenet
=====================

A Pythonic library for Blizzard's Battle.net API for World of Warcraft.

Major features
----------------------

* Pythonic

* Lazyloading and eagerloading

* Eventlet support

Making a connection
----------------------

Global connection settings can be setup so that objects can make connections on the fly.

::

    from battlenet import Connection

    Connection.setup(app='app key')

You can also create connections on the fly.

::

    from battlenet import Connection

    connection = Connection('app key')

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
    realm = Character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.GUILD])

    # Using a specific connection
    realm = connection.get_character(battlenet.UNITED_STATES, 'Nazjatar', 'Vishnevskiy', fields=[Character.GUILD]))

    print character.name
    # => Vishnevskiy

    print character.guild.name
    # => Excellence

More Examples
----------------------

Read the unit tests inside the tests directory.