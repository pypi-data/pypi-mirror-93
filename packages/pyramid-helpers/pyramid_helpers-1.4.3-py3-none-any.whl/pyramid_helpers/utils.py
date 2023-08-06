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

""" Utils functions for Pyramid """

from configparser import ConfigParser
from configparser import Error
from functools import lru_cache
import importlib
import logging
import os
import random
import string

import pytz


RANDOM_STRING = string.ascii_letters + string.digits
TIMEZONE = 'Europe/Paris'


log = logging.getLogger(__name__)


def on_before_renderer(event):
    """ Add utc<->local datetime converters to context """

    request = event['request']

    event['localtoutc'] = request.localtoutc
    event['utctolocal'] = request.utctolocal


def on_new_request(event):
    """ Add utc<->local datetime converters to request """

    request = event.request

    def localtoutc(dt, request=request):
        tzinfo = get_tzinfo(request)
        offset = tzinfo.utcoffset(dt)
        return dt - offset

    request.localtoutc = localtoutc

    def utctolocal(dt, request=request):
        tzinfo = get_tzinfo(request)
        return tzinfo.fromutc(dt)

    request.utctolocal = utctolocal


def get_settings(obj, key, section=None):
    """
    Get settings from key
    If key is missing, try to load settings from `key.filepath` INI file
    """

    registry = obj.registry
    settings = registry.settings

    if key not in settings:
        # Load settings from file
        filepath = settings.get('{0}.filepath'.format(key))
        if filepath is None:
            log.debug('Missing %s.filepath directive, please check configuration file', key)
            return None

        filepath = os.path.abspath(filepath)
        if not os.path.isfile(filepath):
            log.error('Invalid %s.filepath directive, please check configuration file', key)
            return None

        if not os.access(filepath, os.R_OK):
            log.error('Not enough permission to access file %s', filepath)
            return None

        parser = ConfigParser(defaults=dict(here=os.path.dirname(filepath)))
        parser.optionxform = str    # Be case sensitive

        try:
            with open(filepath, 'r') as fp:
                parser.read_file(fp)

            settings[key] = dict(
                (section, dict(parser.items(section)))
                for section in parser.sections()
            )
        except (IOError, Error):
            log.exception('Failed to read file %s', filepath)
            return None

    if section is None:
        return settings[key]

    return settings[key].get(section) or {}


@lru_cache()
def get_tzinfo(request):
    """ Get timezone object """

    # Try to get timezone from authenticated user
    if getattr(request, 'authenticated_user', None) is not None:
        timezone = getattr(request.authenticated_user, 'timezone', None)
    else:
        timezone = None

    if timezone is None or timezone not in pytz.common_timezones:
        # Falling back to timezone from settings
        registry = request.registry
        settings = registry.settings

        timezone = settings.get('timezone')

    if timezone is None or timezone not in pytz.common_timezones:
        # Use default timezone
        timezone = TIMEZONE

    return pytz.timezone(timezone)


def random_string(length=10):
    """ Get a random string """

    return ''.join(
        random.choice(RANDOM_STRING)
        for _ in range(length)
    )


def resolve_dotted(dotted):
    """ Resolve dotted string to module attribute """

    if not dotted:
        return None

    module_name, module_attr = dotted.rsplit('.', 1)
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return None

    return getattr(module, module_attr)


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

    config = Configurator()
    config.include('pyramid_helpers.utils')
    """

    registry = config.registry
    settings = registry.settings

    # Subscribers setup
    config.add_subscriber(on_before_renderer, 'pyramid.events.BeforeRender')
    config.add_subscriber(on_new_request, 'pyramid.events.NewRequest')

    # LDAP configuration
    if settings.get('ldap.enabled', 'false').lower() in ('true', 'yes'):
        config.include('pyramid_helpers.ldap')

    # RADIUS configuration
    if settings.get('radius.enabled', 'false').lower() in ('true', 'yes'):
        config.include('pyramid_helpers.radius')
