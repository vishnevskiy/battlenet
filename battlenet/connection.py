import simplejson
import logging
import urllib2
import os
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

class Connection(object):
    defaults = {
        'eventlet': False,
        'app': None
    }

    def __init__(self, app=None, game='wow', eventlet=None):
        self.app = app or Connection.get_default('app')
        self.game = game
        self.eventlet = eventlet or Connection.get_default('eventlet')

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        
        return self.game == other.game

    def __ne__(self, other):
        return not self.__eq__(other)
    
    @staticmethod
    def setup(**defaults):
        Connection.defaults.update(defaults)

    @staticmethod
    def get_default(name):
        value = Connection.defaults.get(name)
        assert value is not None
        return value

    def make_request(self, region, path, params=None):
        params = params or {}
        params['app'] = self.app

        url = URL_FORMAT % {
            'region': region,
            'game': self.game,
            'path': path,
            'params': '&'.join('='.join((k, ','.join(v) if isinstance(v, (set, list, tuple)) else v))
                for k, v in params.items() if v)
        }

        logger.debug('Battle.net => ' + url)

        try:
            if self.eventlet and eventlet_urllib2:
                response = eventlet_urllib2.urlopen(url)
            else:
                response = urllib2.urlopen(url)
        except urllib2.URLError:
            raise APIError('HTTP 404')

        try:
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

    def get_realm(self, region, name, raw=False):
        data = self.make_request(region, '/realm/status', {'realm': slugify(name)})

        if len(data['realms']) != 1:
            raise RealmNotFound

        if raw:
            return data['realms'][0]

        return Realm(self, region, data=data['realms'][0], connection=self)