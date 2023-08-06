# -*- coding: utf-8 -*-

# pyramid-helpers -- Helpers to develop Pyramid applications
# By: Cyril Lacoux <clacoux@easter-eggs.com>
#     Valéry Febvre <vfebvre@easter-eggs.com>
#
# Copyright (C) 2011-2021 Cyril Lacoux, Easter-eggs
# https://gitlab.com/yack/pyramid-helpers
#
# This file is part of pyramid-helpers.
#
# pyramid-helpers is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pyramid-helpers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" LDAP client for Pyramid-Helpers """

import logging
import pprint
import re
import threading
import time

from beaker.cache import Cache
from beaker.util import NoneType
from beaker.util import parse_cache_config_options
from beaker.util import verify_rules

import ldap
import ldap.controls
import ldap.modlist

from pyramid_helpers.auth import AuthenticationClient
from pyramid_helpers.utils import get_settings


SETTINGS_DEFAULTS = {
    'ldap': {
        'tls': False,
        'auth_base_dn': None,
        'auth_filter': 'uid={0}',
        'base_dn': None,
        'bind_dn': None,
        'bind_credential': None,
        'max_retry': 5,
        'retry_after': 300,
        'timeout': 2.0,
    },
}

SETTINGS_RULES = {
    'ldap': [
        ('uri', (str, NoneType), 'uri must be a string designating valid uri'),
        ('tls', (bool, NoneType), 'tls must be a boolean or an integer'),
        ('auth_base_dn', (str, NoneType), 'auth_base_dn must be a string designating a valid dn'),
        ('auth_filter', (str, NoneType), 'auth_filter must be a string designating a valid filter'),
        ('base_dn', (str, NoneType), 'base_dn must be a string designating a valid dn'),
        ('bind_dn', (str, NoneType), 'bind_dn must be a string designating a valid dn'),
        ('bind_credential', (str, NoneType), 'bind_credential must be a string designating a valid credential'),
        ('max_retry', (int, ), 'max_retry must be a string designating a valid integer'),
        ('retry_after', (int, ), 'retry_after must be a string designating a valid integer'),
        ('timeout', (float, ), 'timeout must be a string designating a valid float'),
    ],
}


log = logging.getLogger(__name__)

client = None


class LDAPClient(AuthenticationClient):
    """ LDAP authentication client """

    # pylint: disable=no-member,too-many-instance-attributes

    __auth_mode__ = 'ldap'

    def __init__(self):
        """ LDAP initialization """

        self.uri = None
        self.tls = False
        self.auth_base_dn = None
        self.auth_filter = None
        self.base_dn = None
        self.__cache = None
        self.__bind_dn = None
        self.__bind_credential = None

        self.__conn = None
        self.__lock = threading.Lock()

        # Error handling
        self.max_retry = 5
        self.retry_after = 300
        self.timeout = 2.0

        self.fail_count = 0
        self.wait_until = None

    def __enter__(self):
        """ Acquire lock """

        self.__lock.acquire()

        return self

    def __exit__(self, type_, value, traceback):
        """ Release lock and close connection """

        self.unbind()
        self.__lock.release()

    def __on_error(self, message, level=logging.ERROR, **kwargs):

        self.fail_count += 1

        if self.fail_count >= self.max_retry:
            self.fail_count = 0
            self.wait_until = time.time() + self.retry_after

            msg = '[LDAP] %s, max failure count was reached (%s), waiting for %s seconds before attempting new connection'
            args = (self.max_retry, self.retry_after)
        else:
            msg = '[LDAP] %s, retry=%s, remaining=%s'
            args = (self.fail_count, self.max_retry - self.fail_count)

        log.log(level, msg, message, *args, **kwargs)

    def add(self, dn, attrs):
        """ Add a new object to LDAP """

        if not self.bind(self.__bind_dn, self.__bind_credential):
            return False

        # Get ldif object suitable for ldap.add()
        ldif = ldap.modlist.addModlist(attrs)
        try:
            # Create LDAP object
            self.__conn.add_s(dn, ldif)
        except ldap.LDAPError:
            log.exception('[LDAP] Failed to create object dn=%s, ldif was:\n%s', dn, pprint.pformat(ldif))
            return False

        log.info('[LDAP] Created object dn=%s.', dn)
        return True

    def bind(self, dn, credential, force=False):
        """ Initialize LDAP connection """

        assert self.__lock.locked(), 'Please use LDAPClient inside a `with` statement'

        if self.__conn is not None and not force:
            return True

        if self.wait_until and self.wait_until > time.time():
            return False

        self.wait_until = None

        try:
            self.__conn = ldap.initialize(self.uri)

            self.__conn.set_option(ldap.OPT_NETWORK_TIMEOUT, self.timeout)
            self.__conn.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
            self.__conn.set_option(ldap.OPT_TIMEOUT, self.timeout)

            if self.tls:
                self.__conn.start_tls_s()

            if dn and credential:
                self.__conn.simple_bind_s(dn, credential)

        except ldap.INVALID_CREDENTIALS:
            log.error('[LDAP] Authentication failed (%s)', dn)
            return False

        except ldap.LDAPError:
            self.__on_error('Failed to connect to remote server', exc_info=1)
            return False

        # Success
        self.fail_count = 0

        return True

    def get(self, dn, attrlist=None, force=False):
        """ Get an object from it's DN """

        result = self.search(attrlist=attrlist, dn=dn, force=force)
        if not result:
            return None

        return result[0]

    def delete(self, dn):
        """ Delete an object from LDAP """

        if not self.bind(self.__bind_dn, self.__bind_credential):
            return False

        try:
            self.__conn.delete_s(dn)
        except ldap.LDAPError:
            log.exception('[LDAP] Failed to delete object dn=%s.', dn)
            return False

        log.info('[LDAP] Deleted object dn=%s.', dn)
        return True

    def modify(self, dn, old_attrs, new_attrs):
        """ Modify an existing object in LDAP """

        if not self.bind(self.__bind_dn, self.__bind_credential):
            return False

        # Get ldif object suitable for ldap.modify()
        ldif = ldap.modlist.modifyModlist(old_attrs, new_attrs, ignore_attr_types=['objectClass', ])
        if not ldif:
            # No modification
            log.debug('[LDAP] Object dn=%s is uptodate', dn)
            return None

        try:
            self.__conn.modify_s(dn, ldif)
        except ldap.LDAPError:
            log.exception('[LDAP] Failed to modify object dn=%s, ldif was:\n%s', dn, pprint.pformat(ldif))
            return False

        log.info('[LDAP] Modified object dn=%s.', dn)
        return True

    # pylint: disable=too-many-arguments
    def search(self, attrlist=None, base_dn=None, dn=None, filterstr='(objectClass=*)', force=False):
        """ Search entries in LDAP """

        if dn is None:
            if base_dn is None:
                base_dn = self.base_dn
            cache_key = '{0}::{1}'.format(base_dn or '', filterstr)
            scope = ldap.SCOPE_SUBTREE
        else:
            base_dn = dn
            cache_key = dn
            scope = ldap.SCOPE_BASE

        if not force and self.__cache is not None:
            try:
                return self.__cache[cache_key]
            except KeyError:
                pass

        if not self.bind(self.__bind_dn, self.__bind_credential):
            return None

        try:
            result = self.__conn.search_s(base_dn, scope, filterstr=filterstr, attrlist=attrlist)
        except ldap.NO_SUCH_OBJECT:
            return None
        except ldap.LDAPError:
            self.__on_error('Failed to query remote server', exc_info=1)
            return None

        if self.__cache is not None:
            self.__cache[cache_key] = result

        return result

    # pylint: disable=too-many-arguments
    def search_iter(self, attrlist=None, base_dn=None, filterstr='(objectClass=*)', size=100):
        """ Search entries in LDAP (paged) """

        if base_dn is None:
            base_dn = self.base_dn

        if not self.bind(self.__bind_dn, self.__bind_credential):
            return

        control = ldap.controls.SimplePagedResultsControl(True, size=size, cookie='')

        while True:
            try:
                msgid = self.__conn.search_ext(base_dn, ldap.SCOPE_SUBTREE, filterstr=filterstr, attrlist=attrlist, serverctrls=[control])
            except ldap.NO_SUCH_OBJECT:
                return
            except ldap.LDAPError:
                self.__on_error('Failed to query remote server', exc_info=1)
                return

            try:
                _, rdata, _, rcontrols = self.__conn.result3(msgid)
            except ldap.LDAPError:
                self.__on_error('Could not pull LDAP results', exc_info=1)
                break

            # Yield result
            for dn, attrs in rdata:
                yield (dn, attrs)

            # Get page control fron returned controls
            for rcontrol in rcontrols:
                if rcontrol.controlType == ldap.CONTROL_PAGEDRESULTS:
                    break
            else:
                self.__on_error('Server ignores RFC 2696 control')
                break

            # pylint: disable=undefined-loop-variable
            if not rcontrol.cookie:
                # No more result
                break

            control.cookie = rcontrol.cookie

    def setup(self, *args, **kwargs):
        """
        LDAP client setup

        :param uri: URI to connect to
        :param tls: Boolean, enable TLS connectiion
        :param auth_base_dn: Base DN for authentication
        :param auth_filter: Filter string for authentication
        :param base_dn: Base DN for searches
        :param bind_dn: Bind DN to use when querying the server
        :param bind_credentiak: Bind credential to use when querying the server
        :param cache: Cache store
        :param max_retry: Integer, maximum retries before stopping to query the server
        :param retry_after: Integer, number of seconds to wait before retrying to query the server
        :param timeout: Float, timeout value for connections
        """

        self.uri = kwargs.get('uri')
        self.tls = kwargs.get('tls', False)

        self.auth_base_dn = kwargs.get('auth_base_dn')
        self.auth_filter = kwargs.get('auth_filter')
        self.base_dn = kwargs.get('base_dn')

        self.__bind_dn = kwargs.get('bind_dn')
        self.__bind_credential = kwargs.get('bind_credential')
        self.__cache = kwargs.get('cache')

        if kwargs.get('max_retry') is not None:
            self.max_retry = kwargs['max_retry']

        if kwargs.get('retry_after') is not None:
            self.retry_after = kwargs['retry_after']

        if kwargs.get('timeout') is not None:
            self.timeout = kwargs['timeout']

        # Calling inherited
        return super().setup(*args, **kwargs)

    def unbind(self):
        """ Close the connection """

        if self.__conn is None:
            return True

        try:
            self.__conn.unbind()

        except ldap.LDAPError:
            self.__on_error('Failed to unbind connection', level=logging.WARNING)
            return False

        finally:
            self.__conn = None

        return True

    def validate_password(self, username, password, request):
        """ Attempt to bind with the LDAP server using simple authentication """

        if not ldap.dn.is_dn(username):
            if self.auth_filter is None:
                # Configuration error
                log.error('[LDAP] Username must either be dn or auth_filter must be set when calling `.validate_password()`')
                return False

            result = self.search(filterstr=self.auth_filter.format(username), base_dn=self.auth_base_dn)
            if not result:
                # Invalid user
                return False

            username = result[0][0]

        self.unbind()

        return self.bind(username, password)


def parse_settings(settings, include_defaults=True):
    """ Parse and check LDAP settings """

    if include_defaults:
        for section in SETTINGS_DEFAULTS:
            if section not in settings:
                settings[section] = SETTINGS_DEFAULTS[section].copy()
                continue

            for option, value in SETTINGS_DEFAULTS[section].items():
                settings[section].setdefault(option, value)

    for section in settings:
        settings[section].pop('here', None)

        for regex in SETTINGS_RULES:
            if re.match(f'^{regex}$', section):
                verify_rules(settings[section], SETTINGS_RULES[regex])
                break

    return settings


# Create client object
client = LDAPClient()


def includeme(config):
    """ LDAP module initialization """

    # Load and parse settings
    settings = get_settings(config, 'ldap')
    if settings is None:
        raise Exception('[LDAP] Invalid or missing configuration for LDAP, please check ldap.filepath directive')

    settings = parse_settings(settings)

    # Connection
    if settings['ldap']['uri'] is None:
        raise Exception('[LDAP] Missing uri parameter in configuration')

    # Cache setup
    cache_params = parse_cache_config_options(dict(
        ('cache.{0}'.format(k), v)
        for k, v in settings['cache'].items()
    )) if 'cache' in settings else dict(enabled=False)

    if cache_params['enabled']:
        cache = Cache('ldap', **cache_params)
    else:
        cache = None

    # Prepare arguments
    kwargs = settings['ldap'].copy()

    # Setup the client
    client.setup(cache=cache, **kwargs)

    log.info('[LDAP] Initialization complete: uri=%s, cache=%s', client.uri, 'yes, type={type}, expire={expire}'.format(**cache_params) if cache else 'no')
