battlenet
=====================

battlenet for Python is a library to interact with Blizzard's Battle.net API for
World of Warcraft.


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

You can allow create connections on the fly.

    from battlenet import Connection

    connection = Connection('app key')

 