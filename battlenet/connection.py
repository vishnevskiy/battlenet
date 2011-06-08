import simplejson
import logging
import urllib2
import os

# used in signing process
import base64
import hmac
import sha
import time

from urlparse import urlparse

from .things import Character, Realm
from .exceptions import APIError, RealmNotFound
from .utils import slugify, quote

try:
    from eventlet.green import urllib2 as eventlet_urllib2
except ImportError:
    eventlet_urllib2 = None

__all__ = ['Connection']

URL_FORMAT = os.environ.get('BATTLENET_URL_FORMAT', 'http://%(region)s.battle.net/api/%(game)s%(path)s?%(params)s')

logger = logging.getLogger('battlenet')

WDAY = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
MON = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

class Connection(object):
    defaults = {
        'eventlet': False,
        'public_key': None,
        'private_key': None
    }

    def __init__(self, public_key = None, private_key = None, game='wow', eventlet=None):
        self.public_key = public_key or  Connection.defaults.get('public_key', None)
        self.private_key = private_key or  Connection.defaults.get('private_key', None)
        self.game = game
        self.eventlet = eventlet or Connection.defaults.get('eventlet', False)

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False

        return self.game == other.game

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def setup(**defaults):
        Connection.defaults.update(defaults)

    def sign(self, method, now, url, private_key):
        string_to_sign = '%s\n%s\n%s\n' % (method, now, url)
        return base64.encodestring(hmac.new(private_key, string_to_sign, sha).digest()).rstrip()

    def make_request(self, region, path, params=None):
        params = params or {}

        now = time.gmtime()
        date = '%s, %2d %s %d %2d:%02d:%02d GMT' % (WDAY[now[6]], now[2], MON[now[1]], now[0], now[3], now[4], now[5])
        headers = { 'Date': date }

        url = URL_FORMAT % {
            'region': region,
            'game': self.game,
            'path': path,
            'params': '&'.join('='.join((k, ','.join(v) if isinstance(v, (set, list, tuple)) else v))
                for k, v in params.items() if v)
        }

        uri = urlparse(url)

        if self.public_key:
            signature = self.sign('GET', date, uri.path, self.private_key)
            headers['Authorization'] = 'BNET %s:%s' % (self.public_key, signature)

        logger.debug('Battle.net => ' + url)

        try:
            request = urllib2.Request(url, None, headers)
            if self.eventlet and eventlet_urllib2:
                response = eventlet_urllib2.urlopen(request)
            else:
                response = urllib2.urlopen(request)
        except urllib2.URLError:
            raise APIError('HTTP 404')

        try:
            print response
            data = simplejson.loads(response.read())
        except simplejson.JSONDecodeError:
            raise APIError('Non-JSON Response')
        else:
            if data.get('status') == 'nok':
                raise APIError(data['reason'])

        return data

    def get_character(self, region, realm, name, fields=None, raw=False):
        name = quote(name.lower())
        realm = slugify(realm)

        data = self.make_request(region, '/character/%s/%s' % (realm, name), {'fields': fields})

        if raw:
            return data

        return Character(region, data=data, connection=self)

    def get_all_realms(self, region, raw=False):
        data = self.make_request(region, '/realm/status')

        if raw:
            return data['realms']

        return [Realm(region, data=realm, connection=self) for realm in data['realms']]

    def get_realms(self, region, names, raw=False):
        data = self.make_request(region, '/realm/status', {'realms': ','.join(map(slugify, names))})

        if raw:
            return data['realms']

        return [Realm(region, data=realm, connection=self) for realm in data['realms']]

    def get_realm(self, region, name, raw=False):
        data = self.make_request(region, '/realm/status', {'realm': slugify(name)})

        if len(data['realms']) != 1:
            raise RealmNotFound

        if raw:
            return data['realms'][0]

        return Realm(self, region, data=data['realms'][0], connection=self)
