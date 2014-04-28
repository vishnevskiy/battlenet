import logging
import urllib2
import urllib
import base64
import hmac
import hashlib
import time
import urlparse
import re
from .things import Character, Realm, Guild, Reward, Perk, Class, Race
from .exceptions import APIError, CharacterNotFound, GuildNotFound, RealmNotFound
from .utils import quote, normalize

try:
    import simplejson as json
except ImportError:
    import json


__all__ = ['Connection']

URL_FORMAT = 'https://%(region)s.battle.net/api/%(game)s%(path)s?%(params)s'

logger = logging.getLogger('battlenet')

DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',)
MONTHS = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)


class Connection(object):
    defaults = {
        'public_key': None,
        'private_key': None,
        'locale': 'en_US'
    }

    def __init__(self, public_key=None, private_key=None, game='wow', locale=None):
        self.public_key = public_key or Connection.defaults.get('public_key')
        self.private_key = private_key or Connection.defaults.get('private_key')
        self.game = game
        self.locale = locale or Connection.defaults.get('locale')

        self._cache = {}

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False

        return self.game == other.game

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def setup(**defaults):
        Connection.defaults.update(defaults)

    def sign_request(self, method, now, url, private_key):
        string_to_sign = '%s\n%s\n%s\n' % (method, now, url)
        hash = hmac.new(private_key, string_to_sign, hashlib.sha1).digest()
        return base64.encodestring(hash).rstrip()

    def make_request(self, region, path, params=None, cache=False):
        params = params or {}
        params['locale'] = self.locale

        now = time.gmtime()
        date = '%s, %2d %s %d %2d:%02d:%02d GMT' % (DAYS[now[6]], now[2],
            MONTHS[now[1]], now[0], now[3], now[4], now[5])

        headers = {
            'Date': date
        }

        url = URL_FORMAT % {
            'region': region,
            'game': self.game,
            'path': path,
            'params': '&'.join('='.join(
                (k, ','.join(v) if isinstance(v, (set, list)) else v))
                for k, v in params.items() if v)
        }

        if cache and url in self._cache:
            return self._cache[url]

        uri = urlparse.urlparse(url)
        if self.public_key:
            signature = self.sign_request('GET', date, uri.path, self.private_key)
            headers['Authorization'] = 'BNET %s:%s' % (self.public_key, signature)

        logger.debug('Battle.net => ' + url)

        request = urllib2.Request(url, None, headers)

        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            raise APIError(str(e))

        try:
            data = json.loads(response.read())
        except json.JSONDecodeError:
            raise APIError('Non-JSON Response')
        else:
            if data.get('status') == 'nok':
                raise APIError(data['reason'])

        if cache:
            self._cache[url] = data

        return data

    def clean_realm(self, realm):
        realm = re.sub('[()]', '', realm)
        return quote(realm.lower()).replace("%20", '-')

    def get_character(self, region, realm, name, fields=None, raw=False):
        name = quote(name.lower())
        realm = self.clean_realm(realm)

        try:
            data = self.make_request(region, '/character/%s/%s' % (realm, name), {'fields': fields})

            if not data:
                raise CharacterNotFound
                
            if raw:
                return data

            return Character(region, data=data, connection=self)
        except APIError:
            raise CharacterNotFound

    def get_guild(self, region, realm, name, fields=None, raw=False):
        name = quote(name.lower())
        realm = self.clean_realm(realm)

        try:
            data = self.make_request(region, '/guild/%s/%s' % (realm, name), {'fields': fields})

            if raw:
                return data

            return Guild(region, data=data, connection=self)
        except APIError:
            raise GuildNotFound

    def get_all_realms(self, region, raw=False):
        data = self.make_request(region, '/realm/status')

        if raw:
            return data['realms']

        return [Realm(region, data=realm, connection=self) for realm in data['realms']]

    def get_realms(self, region, names, raw=False):
        data = self.make_request(region, '/realm/status', {'realms': ','.join(map(quote, names))})

        if raw:
            return data['realms']

        return [Realm(region, data=realm, connection=self) for realm in data['realms']]

    def get_realm(self, region, name, raw=False):
        data = self.make_request(region, '/realm/status', {'realm': quote(name.lower())})
        data = [d for d in data['realms'] if normalize(d['name']) == normalize(name)]

        if len(data) != 1:
            raise RealmNotFound

        if raw:
            return data[0]

        return Realm(self, region, data=data[0], connection=self)

    def get_guild_perks(self, region, raw=False):
        data = self.make_request(region, '/data/guild/perks', cache=True)
        perks = data['perks']

        if raw:
            return perks

        return [Perk(region, perk) for perk in perks]

    def get_guild_rewards(self, region, raw=False):
        data = self.make_request(region, '/data/guild/rewards', cache=True)
        rewards = data['rewards']

        if raw:
            return rewards

        return [Reward(region, reward) for reward in rewards]

    def get_character_classes(self, region, raw=False):
        data = self.make_request(region, '/data/character/classes', cache=True)
        classes = data['classes']

        if raw:
            return classes

        return [Class(class_) for class_ in classes]

    def get_character_races(self, region, raw=False):
        data = self.make_request(region, '/data/character/races', cache=True)
        races = data['races']

        if raw:
            return races

        return [Race(race) for race in races]

    def get_item(self, region, item_id, raw=False):
        data = self.make_request(region, '/item/%d' % item_id)
        return data
