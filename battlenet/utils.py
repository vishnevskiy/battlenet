import unicodedata
import re
import urllib

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    
    if not isinstance(value, unicode):
        value = unicode(value)

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())

    return _slugify_hyphenate_re.sub('-', value)

def normalize(name):
    if isinstance(name, str):
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