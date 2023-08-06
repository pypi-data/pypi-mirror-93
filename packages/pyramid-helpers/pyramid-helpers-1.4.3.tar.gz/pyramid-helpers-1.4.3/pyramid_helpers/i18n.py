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

""" I18n helpers for Pyramid """

from babel.dates import format_date as format_date_
from babel.dates import format_time as format_time_
from babel.numbers import format_decimal as format_decimal_


def N_(tstring):
    """ Dummy translation function """
    return tstring


def add_renderer_globals(event):
    """ Add _() function to renderer context """
    request = event['request']
    event['_'] = request.translate
    event['ungettext'] = request.pluralize
    event['localizer'] = request.localizer
    event['format_date'] = request.format_date
    event['format_datetime'] = request.format_datetime
    event['format_decimal'] = request.format_decimal
    event['format_time'] = request.format_time


def add_localizer(event):
    """ Add localizer to request """
    request = event.request
    registry = request.registry
    settings = registry.settings or {}

    domain = settings.get('i18n.domain')
    localizer = request.localizer

    # Tanslations
    def auto_translate(tstring, domain=domain):
        return localizer.translate(tstring, domain=domain)

    def auto_pluralize(singular, plural, num, domain=domain):
        return localizer.pluralize(singular, plural, num, domain=domain)

    request.translate = auto_translate
    request.pluralize = auto_pluralize

    # Localize some Babel functions
    def format_date(dt, *args, **kwargs):
        return format_date_(dt, *args, locale=localizer.locale_name, **kwargs)

    def format_datetime(dt, *args, **kwargs):
        date_format = kwargs.pop('date_format', 'long')
        time_format = kwargs.pop('time_format', 'short')
        return '{0} {1}'.format(
            format_date(dt, *args, format=date_format, **kwargs),
            format_time(dt, *args, format=time_format, **kwargs),
        )

    def format_decimal(number, *args, **kwargs):
        return format_decimal_(number, *args, locale=localizer.locale_name, **kwargs)

    def format_time(dt, *args, **kwargs):
        return format_time_(dt, *args, locale=localizer.locale_name, **kwargs)

    request.format_date = format_date
    request.format_datetime = format_datetime
    request.format_decimal = format_decimal
    request.format_time = format_time


def header_locale_negotiator(request):
    """ Locale negotiation from Accept-Language header """
    registry = request.registry
    settings = registry.settings or {}
    available_languages = settings.get('i18n.available_languages', '').split()
    default_locale_name = settings.get('i18n.default_locale_name', 'en')

    locale_name = None
    if request.accept_language:
        locale_name = request.accept_language.best_match(available_languages)

    if locale_name is None:
        locale_name = default_locale_name

    return locale_name


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

    config = Configurator()
    config.include('pyramid_helpers.i18n')
    """

    registry = config.registry
    settings = registry.settings

    if settings.get('i18n.enabled', 'false').lower() not in ('true', 'yes'):
        return

    config.set_locale_negotiator(header_locale_negotiator)
    config.add_subscriber(add_renderer_globals, 'pyramid.events.BeforeRender')
    config.add_subscriber(add_localizer, 'pyramid.events.NewRequest')

    directories = settings.get('i18n.directories')
    if not directories:
        return

    for directory in directories.split():
        config.add_translation_dirs(directory)
