import unicodedata
import urllib


def normalize(name):
    if not isinstance(name, unicode):
        name = name.decode('utf-8')

    name = name.replace("'", '')
    return ''.join(c for c in unicodedata.normalize('NFD', name)
           if unicodedata.category(c) != 'Mn').encode('utf-8')


def quote(name):
    if isinstance(name, unicode):
        name = normalize(name)

    return urllib.quote(name)


def make_icon_url(region, icon, size='large'):
    if not icon:
        return ''

    if size == 'small':
        size = 18
    else:
        size = 56

    return 'http://%s.media.blizzard.com/wow/icons/%d/%s.jpg' % (region, size, icon)


def make_connection():
    if not hasattr(make_connection, 'Connection'):
        from .connection import Connection
        make_connection.Connection = Connection

    return make_connection.Connection()
