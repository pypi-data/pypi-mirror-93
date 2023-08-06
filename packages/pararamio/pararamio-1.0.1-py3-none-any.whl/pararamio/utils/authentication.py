import base64
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime
from http.cookiejar import CookieJar
from typing import Any, Dict, Tuple, cast
from urllib.error import HTTPError

from pararamio._types import HeaderLikeT
from pararamio.constants import XSRF_HEADER_NAME
from pararamio.exceptions import PararamioAuthenticationException, PararamioXSFRRequestError
from pararamio.utils.requests import api_request, raw_api_request


__all__ = ('get_xsrf_token',)

XSFR_URL = INIT_URL = '/auth/init'
LOGIN_URL = '/auth/login/password'
TWO_STEP_URL = '/auth/totp'
AUTH_URL = '/auth/next'
log = logging.getLogger('pararamio')


def get_xsrf_token(cookie_jar: CookieJar) -> str:
    _, headers = raw_api_request(XSFR_URL, cookie_jar=cookie_jar)
    for key, value in headers:
        if key == 'X-Xsrftoken':
            return value
    raise PararamioXSFRRequestError('XSFR Header was not found in %s url' % XSFR_URL)


def do_init(cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            INIT_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_login(login: str, password: str, cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            LOGIN_URL,
            method='POST',
            data={'email': login, 'password': password},
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_taking_secret(cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            AUTH_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_second_step(key: str, cookie_jar: CookieJar, headers: dict) -> Tuple[bool, Dict[str, str]]:
    resp = api_request(
        TWO_STEP_URL,
        method='POST',
        data={'code': generate_otp(key)},
        headers=headers,
        cookie_jar=cookie_jar,
    )
    return True, resp


def authenticate(login: str, password: str, cookie_jar: CookieJar, key: str = None, headers: HeaderLikeT = None) -> Tuple[bool, Dict[str, Any], str]:
    if not headers or XSRF_HEADER_NAME not in headers:
        if headers is None:
            headers = {}
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)

    success, resp = do_login(login, password, cookie_jar, headers)

    if not success and resp.get('error', 'xsrf'):
        log.debug('invalid xsrf trying to get new one')
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)
        success, resp = do_login(login, password, cookie_jar, headers)

    if not success:
        log.error('authentication failed: %s', resp.get('error', ''))
        raise PararamioAuthenticationException('login, password authentication failed')

    if key:
        success, resp = do_second_step(key, cookie_jar, headers)
        if not success:
            raise PararamioAuthenticationException('Second factor authentication failed')

    success, resp = do_taking_secret(cookie_jar, headers)

    if not success:
        raise PararamioAuthenticationException('Taking secret failed')

    success, resp = do_init(cookie_jar, headers)

    return True, {'user_id': resp.get('user_id')}, headers[XSRF_HEADER_NAME]


def generate_otp(key: str) -> str:
    digits = 6
    digest = hashlib.sha1
    interval = 30

    def byte_secret(s):
        missing_padding = len(s) % 8
        if missing_padding != 0:
            s += '=' * (8 - missing_padding)
        return base64.b32decode(s, casefold=True)

    def int_to_byte_string(i, padding=8):
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

    def time_code(for_time):
        i = time.mktime(for_time.timetuple())
        return int(i / interval)

    hmac_hash = hmac.new(
        byte_secret(key),
        int_to_byte_string(time_code(datetime.now())),
        digest,
    ).digest()

    hmac_hash = bytearray(hmac_hash)
    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 | (hmac_hash[offset + 1] & 0xff) << 16 | (hmac_hash[offset + 2] & 0xff) << 8 | (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = '0' + str_code

    return str_code
