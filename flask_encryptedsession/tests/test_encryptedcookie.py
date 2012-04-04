# -*- coding: utf-8 -*-
"""
    flask_encryptedsession.tests.test_encryptedcookie
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests the encrypted cookie.

    :license: BSD, see LICENSE for more details.
"""
import unittest

from werkzeug.testsuite import WerkzeugTestCase

from werkzeug.utils import parse_cookie
from werkzeug.wrappers import Request, Response

from flask_encryptedsession.encryptedcookie import EncryptedCookie


KEYS_DIR = '/tmp/keys'
KEYS_DIR_BAD = '/tmp/badkeys'


class EncryptedCookieTestCase(WerkzeugTestCase):

    def test_basic_support(self):
        c = EncryptedCookie(keys_location=KEYS_DIR)
        assert c.new
        assert not c.modified
        assert not c.should_save
        c['x'] = 42
        assert c.modified
        assert c.should_save
        s = c.serialize()

        c2 = EncryptedCookie.unserialize(s, KEYS_DIR)
        assert c is not c2
        assert not c2.new
        assert not c2.modified
        assert not c2.should_save
        assert c2 == c

        c3 = EncryptedCookie.unserialize(s, KEYS_DIR_BAD)
        assert not c3.modified
        assert not c3.new
        assert c3 == {}

    def test_wrapper_support(self):
        req = Request.from_values()
        resp = Response()
        c = EncryptedCookie.load_cookie(req, keys_location=KEYS_DIR)
        assert c.new
        c['foo'] = 42
        assert c.keys_location == KEYS_DIR
        c.save_cookie(resp)

        req = Request.from_values(headers={
            'Cookie':  'session="%s"' % parse_cookie(resp.headers['set-cookie'])['session']
        })
        c2 = EncryptedCookie.load_cookie(req, keys_location=KEYS_DIR)
        assert not c2.new
        assert c2 == c


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EncryptedCookieTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()