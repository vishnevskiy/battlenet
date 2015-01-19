"""
battlenet test fixtures

"""

import pytest
import battlenet.connection
import time
import urllib2
from mock import patch, MagicMock, call

def connection_throwing_urlerror(urlliberror, bnet_error_class, fname, fargs):
    tval = time.gmtime(1421676160)
    tval_s = 'Mon, 19 Jan 2015 14:02:40 GMT'
    mock_req = MagicMock(spec_set=urllib2.Request)
    with patch('battlenet.connection.urllib2.urlopen', autospec=True) as mock_urlopen, \
         patch('battlenet.connection.urllib2.Request', autospec=True) as mock_request, \
         patch('battlenet.connection.time.gmtime', autospec=True) as mock_gmtime:
        mock_gmtime.return_value = tval
        mock_urlopen.side_effect = urlliberror
        mock_request.return_value = mock_req
        conn = battlenet.connection.Connection()
        res = None
        with pytest.raises(bnet_error_class) as raised:
            fn = getattr(conn, fname)
            if len(fargs) == 2:
                res = fn(fargs[0], fargs[1])
            else:
                res = fn(fargs[0], fargs[1], fargs[2])
        return (conn, tval_s, mock_urlopen, mock_req, mock_request, res, raised)
