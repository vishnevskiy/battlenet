import unicodedata
import re
import urllib

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


def slugify(value):
    slug = unicode(_slugify_strip_re.sub('', normalize(value)).strip().lower())
    slug = _slugify_hyphenate_re.sub('-', slug)

    if not slug:
        return quote(value)

    return quote(slug)


def normalize(name):
    if not isinstance(name, unicode):
        name = name.decode('utf8')

    return unicodedata.normalize('NFKC', name).encode('utf8')


def quote(name):
    return urllib.quote(normalize(name))


def make_icon_url(region, icon, size='large'):
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
