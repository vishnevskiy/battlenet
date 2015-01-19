import os
import urllib2
import pytest
from mock import patch, MagicMock, call
import time

import battlenet
from battlenet.tests.fixtures import *

class Test_Exceptions:

    def test_character_not_found(self):
        f = connection_throwing_urlerror(urllib2.URLError("foo"),
                                         battlenet.CharacterNotFound,
                                         'get_character',
                                         (battlenet.UNITED_STATES, 'Fake Realm', 'Fake Character'))
        conn, tval_s, mock_urlopen, mock_req, mock_request, res, raised = f
        assert raised.typename == 'CharacterNotFound'
        assert mock_urlopen.mock_calls == [call(mock_req)]
        assert mock_req.mock_calls == []
        url = 'https://us.battle.net/api/wow/character/fake-realm/fake%20character?locale=en_US'
        assert mock_request.mock_calls == [call(url, None, {'Date': 'Mon, 19 Jan 2015 14:02:40 GMT'})]

    def test_guild_not_found(self):
        f = connection_throwing_urlerror(urllib2.URLError("foo"),
                                         battlenet.GuildNotFound,
                                         'get_guild',
                                         (battlenet.UNITED_STATES, 'Fake Realm', 'Fake Guild'))
        conn, tval_s, mock_urlopen, mock_req, mock_request, res, raised = f
        assert raised.typename == 'GuildNotFound'
        assert mock_urlopen.mock_calls == [call(mock_req)]
        assert mock_req.mock_calls == []
        url = 'https://us.battle.net/api/wow/guild/fake-realm/fake%20guild?locale=en_US'
        assert mock_request.mock_calls == [call(url, None, {'Date': 'Mon, 19 Jan 2015 14:02:40 GMT'})]

    def test_realm_not_found(self):
        f = connection_throwing_urlerror(urllib2.URLError("foo"),
                                         battlenet.RealmNotFound,
                                         'get_realm',
                                         (battlenet.UNITED_STATES, 'Fake Realm'))
        conn, tval_s, mock_urlopen, mock_req, mock_request, res, raised = f
        assert raised.typename == 'RealmNotFound'
        assert mock_urlopen.mock_calls == [call(mock_req)]
        assert mock_req.mock_calls == []
        url = 'https://us.battle.net/api/wow/realm/status?locale=en_US&realm=fake%20realm'
        assert mock_request.mock_calls == [call(url, None, {'Date': 'Mon, 19 Jan 2015 14:02:40 GMT'})]
