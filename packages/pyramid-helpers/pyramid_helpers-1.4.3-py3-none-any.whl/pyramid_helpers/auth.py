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


"""
Authentication module for Pyramid-Helpers

Useful documentation can be found at:
 * https://docs.pylonsproject.org/projects/pyramid/en/latest/api/security.html
 * https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/auth/index.html
"""

import hashlib
import logging

from beaker.util import NoneType
from beaker.util import verify_rules

from pyramid.authentication import AuthTktCookieHelper
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authentication import extract_http_basic_credentials
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.interfaces import IAuthenticationPolicy

from zope.interface import implementer

from pyramid_helpers.utils import get_settings
from pyramid_helpers.utils import resolve_dotted


AUTH_CLIENTS = {}

SETTINGS_DEFAULTS = {
    'auth': {
        'policies': ['ticket', ],
        'mode': None,
        'callback': 'pyramid_helpers.auth.authentication_callback',
        'get_user_by_username': None,
    },
    'policy:basic': {
        'realm': 'Pyramid-Helpers Application',
    },
    'policy:remote': {
        'fake_user': None,
        'login_url': None,
        'logout_url': None,
    },
    'policy:ticket': {
        'secret': 'the-big-secret-for-secured-authentication',
        'hashalg': 'sha512',
    },
    'policy:token': {
        'header': 'X-PH-Authentication-Token',
        'query_param': None,
        'get_username_by_token': None,
    },
}

SETTINGS_RULES = {
    'auth': [
        ('enabled', (bool, NoneType), 'enabled must be a boolean or an integer'),
        ('policies', (list, NoneType), 'policies must be a comma separated list of policies'),
        ('mode', (str, NoneType), 'mode must be a string designating a valid mode'),
        ('callback', (str, NoneType), 'callback must be a string designating a valid callback'),
        ('get_user_by_username', (str,), 'get_user_by_username must be a string designating a valid callback'),
    ],
    'policy:basic': [
        ('realm', (str, NoneType), 'realm must be a string designating a realm authentication'),
    ],
    'policy:remote': [
        ('fake_user', (str, NoneType), 'fake_user must be a string designating a username'),
        ('login_url', (str, NoneType), 'login_url must be a string designating a valid url'),
        ('logout_url', (str, NoneType), 'logout_url must be a string designating a valid url'),
    ],
    'policy:ticket': [
        ('secret', (str, NoneType), 'secret must be a string designating a secret'),
        ('hashalg', (str, NoneType), 'hashalg must be a string designating a valid hashalg'),
    ],
    'policy:token': [
        ('header', (str, NoneType), 'header must be a string designating a HTTP header'),
        ('query_param', (str, NoneType), 'query_param must be a string designating a query parameter'),
        ('get_username_by_token', (str, NoneType), 'get_user_by_token must be a string designating a valid callback'),
    ],
}


log = logging.getLogger(__name__)


class AuthenticationClient:
    """ Authentication client base class """

    __auth_mode__ = None

    def __enter__(self):
        """
        This method is called by the `with:` statement and should be overriden
        to execute some tasks **before** validating the password.
        """

        return self

    def __exit__(self, type_, value, traceback):
        """
        This method is called by the `with:` statement and should be overriden
        to execute some tasks **after** validating the password.
        """

    # pylint: disable=unused-argument
    def setup(self, *args, **kwargs):
        """ Register authentication client """

        if self.__auth_mode__ is None:
            log.error('[AUTH] Attribute `.__auth_mode__` of AuthenticationClient instance must be set')
            return False

        if self.__auth_mode__ in AUTH_CLIENTS:
            log.error('[AUTH] An authentication client is already registered for mode %s', self.__auth_mode__)
            return False

        # Registering object
        AUTH_CLIENTS[self.__auth_mode__] = self

        log.info('[AUTH] Registered authentication client, mode=%s, client=%s', self.__auth_mode__, self.__class__.__name__)

        return True

    def validate_password(self, username, password, request):
        """ Please, override this method to implement the password validation """

        raise NotImplementedError()


@implementer(IAuthenticationPolicy)
class MultiAuthenticationPolicy(CallbackAuthenticationPolicy):
    """
    A Pyramid authentication policy that implements the following protocols:
     * ticket
     * remote
     * basic
     * token
    """

    POLICIES = ['ticket', 'remote', 'basic', 'token']

    # pylint: disable=too-many-arguments
    def __init__(self, callback, policies, hashalg='sha512', realm='Pyramid Helpers', secret=None):

        for policy in policies:
            assert policy in self.POLICIES, '[AUTH] Invalid policy: {0}'.format(policy)

        self.cookie = AuthTktCookieHelper(secret, hashalg=hashalg) if 'ticket' in policies else None
        self.policies = policies
        self.realm = realm

        self.__callback = callback

    def callback(self, username, request):
        """ Custom method that handles multiple authentication mechanisms """

        if request.authentication_policy == 'basic':
            credentials = extract_http_basic_credentials(request)
            if credentials is None:
                return None

            if not check_credentials(credentials.username, credentials.password, request):
                return None

        return self.__callback(username, request)

    def forget(self, request):
        """ Custom method that handles multiple authentication mechanisms """

        if request.authentication_policy == 'basic':
            # Ask client to re-authenticate
            return [('WWW-Authenticate', 'Basic realm="%s"' % self.realm)]

        if self.cookie:
            # Delete cookie
            return self.cookie.forget(request)

        return []

    def remember(self, request, username, **kw):
        """
        Custom method that handles multiple authentication mechanisms

        Accepts the following kw args: ``max_age=<int-seconds>, ``tokens=<sequence-of-ascii-strings>``.
        """

        if request.authentication_policy != 'ticket':
            # Do nothing
            return []

        # Set cookie
        return self.cookie.remember(request, username, **kw)

    def unauthenticated_userid(self, request):
        """ Custom method that handles multiple authentication mechanisms """

        # Extract data
        credentials = extract_http_basic_credentials(request)
        policy = request.headers.get('X-PH-Authentication-Policy')
        remote_user = request.environ.get('REMOTE_USER')
        token = extract_token(request)

        # Guess and check policy
        if policy is None:
            if remote_user:
                policy = 'remote'

            elif credentials:
                policy = 'basic'

            elif token:
                policy = 'token'

            elif self.cookie:
                policy = 'ticket'

        if policy not in self.policies:
            policy = self.policies[0]

        # Store policy to request
        # Policy may be set by the fake user tween
        if getattr(request, 'authentication_policy', None) is None:
            request.authentication_policy = policy

        if policy == 'basic':
            if credentials is None:
                return None

            return credentials.username

        if policy == 'remote':
            return remote_user

        if policy == 'token':
            return get_username_by_token(token, request)

        # Ticket
        result = self.cookie.identify(request)
        if result:
            return result['userid']

        return None


# pylint: disable=unused-argument
def auth_fake_user_tween_factory(handler, registry):
    """
    Tween that adds a fake user to environ to simulate remote user based
    authentication.
    """

    def auth_fake_user_tween(request):
        # Get fake user from settings
        registry = request.registry
        settings = registry.settings
        username = settings['auth']['policy:remote']['fake_user']

        # Add fake user as REMOTE_USER if requested
        environ = request.environ
        environ['REMOTE_USER'] = username

        # Set the authentication policy
        request.authentication_policy = 'fake_user'

        return handler(request)

    return auth_fake_user_tween


def authentication_callback(username, request):
    """ Called by authentication policy when user is authenticated """

    user = get_user_by_username(username, request)
    if user is None:
        # Invalid user
        return None

    return [
        ('group:{0}'.format(group.name))
        for group in user.groups
    ]


def check_credentials(username, password, request):
    """ Check extracted credential using configured mode """

    params = get_settings(request, 'auth', 'auth')

    auth_client = AUTH_CLIENTS.get(params['mode'])
    if auth_client is None:
        # Invalid mode
        return False

    with auth_client as client:
        return client.validate_password(username, password, request)


def extract_token(request):
    """ Extract authentication token from request """

    params = get_settings(request, 'auth', 'policy:token')

    if params.get('query_param'):
        return request.GET.get(params['query_param'])

    if params.get('header'):
        return request.headers.get(params['header'])

    return None


def get_user_by_username(username, request):
    """ Wrapper to get_user_by_username function defined in settings """

    params = get_settings(request, 'auth', 'auth')
    func = params['get_user_by_username']

    return func(username, request)


def get_username_by_token(token, request):
    """ Wrapper to get_username_by_token function defined in settings """

    params = get_settings(request, 'auth', 'auth')
    func = params['get_username_by_token']

    return func(token, request)


def on_before_renderer(event):
    """ Add authenticated_user and has_permission() to renderer context """

    request = event['request']

    event['authentication_policy'] = request.authentication_policy
    event['authenticated_user'] = request.authenticated_user
    event['has_permission'] = request.has_permission


def on_new_request(event):
    """ Add authenticated_user to request """

    request = event.request
    request.authenticated_user = get_user_by_username(request.authenticated_userid, request)

    if not hasattr(request, 'authentication_policy'):
        request.authentication_policy = None


def parse_settings(settings, include_defaults=True):
    """ Parse and check authentication settings """

    if include_defaults:
        for section in SETTINGS_DEFAULTS:
            if section not in settings:
                settings[section] = SETTINGS_DEFAULTS[section].copy()
                continue

            for option, value in SETTINGS_DEFAULTS[section].items():
                settings[section].setdefault(option, value)

    for section, rules in SETTINGS_RULES.items():
        if section in settings:
            verify_rules(settings[section], rules)

    # Check policies
    if 'all' in settings['auth']['policies']:
        settings['auth']['policies'] = MultiAuthenticationPolicy.POLICIES[:]
    else:
        for policy in settings['auth']['policies']:
            if policy not in MultiAuthenticationPolicy.POLICIES:
                raise Exception('[AUTH] Invalid policy for parameters policies in section [auth]: {0}'.format(policy))

    # Check mode
    if settings['auth']['mode'] is None:
        raise Exception('[AUTH] Missing value for parameter mode in section [auth]')

    if settings['auth']['mode'] not in AUTH_CLIENTS:
        raise Exception('[AUTH] Invalid value for parameter mode in section [auth]: {0}'.format(settings['auth']['mode']))

    # Check hashalg
    if settings['policy:ticket']['hashalg'] not in hashlib.algorithms_available:
        raise Exception('[AUTH] Invalid value for parameter hashalg in section [policy:ticket]: {0}'.format(settings['auth']['policy:ticket']['hashalg']))

    # Resolve authentication callback
    func = resolve_dotted(settings['auth']['callback'])
    if func is None:
        raise Exception('[AUTH] Invalid callback: {0}'.format(settings['auth']['callback']))
    settings['auth']['callback'] = func

    # Resolve get_user_by_username
    func = resolve_dotted(settings['auth']['get_user_by_username'])
    if func is None:
        raise Exception('[AUTH] Invalid value for parameter get_user_by_username in section [auth]: {0}'.format(settings['auth']['get_user_by_username']))
    settings['auth']['get_user_by_username'] = func

    # Resolve get_username_by_token if needed
    if 'token' in settings['auth']['policies']:
        func = resolve_dotted(settings['policy:token']['get_username_by_token'])
        if func is None:
            raise Exception('[AUTH] Invalid value for parameter get_username_by_token in section [policy:token]: {0}'.format(settings['auth']['get_username_by_token']))
        settings['policy:token']['get_username_by_token'] = func

    return settings


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

    config = Configurator()
    config.include('pyramid_helpers.auth')
    """

    config.add_subscriber(on_before_renderer, 'pyramid.events.BeforeRender')
    config.add_subscriber(on_new_request, 'pyramid.events.NewRequest')

    # Load an parse settings
    settings = get_settings(config, 'auth')
    if settings is None:
        raise Exception('[AUTH] Invalid or missing configuration for AUTH, please check auth.filepath directive')

    settings = parse_settings(settings)

    # Add fake user tween if needed
    if 'remote' in settings['auth']['policies'] and settings['policy:remote']['fake_user'] is not None:
        log.warning('[AUTH] POLICY `remote` IS ENABLED WITH `fake_user` SET TO `%s`, USER `%s` WILL BE AUTOMATICALLY CONNECTED WITHOUT ANY AUTHENTICATION, THIS IS VERY DANGEROUS !!!', settings['policy:remote']['fake_user'], settings['policy:remote']['fake_user'])

        config.add_tween('pyramid_helpers.auth.auth_fake_user_tween_factory')

    # Set authentication policy
    config.set_authentication_policy(MultiAuthenticationPolicy(
        settings['auth']['callback'],
        settings['auth']['policies'],
        hashalg=settings['policy:ticket']['hashalg'],
        realm=settings['policy:basic']['realm'],
        secret=settings['policy:ticket']['secret'],
    ))

    # Set authorization policy
    config.set_authorization_policy(ACLAuthorizationPolicy())

    log.info('[AUTH] Initialization complete: policies=%s, mode=%s', settings['auth']['policies'], settings['auth']['mode'])
