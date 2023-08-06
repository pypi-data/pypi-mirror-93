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

# pylint: disable=unused-import,redefined-builtin

""" Form tags for Pyramid """


#
# Import standard input types
#
from webhelpers2.html.tags import checkbox      # Noqa: F401
from webhelpers2.html.tags import end_form      # Noqa: F401
from webhelpers2.html.tags import file          # Noqa: F401
from webhelpers2.html.tags import form          # Noqa: F401
from webhelpers2.html.tags import hidden        # Noqa: F401
from webhelpers2.html.tags import password      # Noqa: F401
from webhelpers2.html.tags import radio         # Noqa: F401
from webhelpers2.html.tags import select        # Noqa: F401
from webhelpers2.html.tags import submit        # Noqa: F401
from webhelpers2.html.tags import text          # Noqa: F401
from webhelpers2.html.tags import textarea      # Noqa: F401

from webhelpers2.html.tags import OptGroup      # Noqa: F401
from webhelpers2.html.tags import Option        # Noqa: F401
from webhelpers2.html.tags import Options       # Noqa: F401


def coerce_bool(value):
    """ Coerce pseudo boolean to boolean """

    if isinstance(value, str):
        return value.lower() in ('yes', 'true', '1', 'on')

    if isinstance(value, bool):
        return value

    raise TypeError('{0!r} could not be coerced to boolean'.format(value))


def html_attrs(**attrs):
    """ Format and clean HTML attributes """

    for key, value in list(attrs.items()):
        if key in ('disabled', 'readonly'):
            if value.lower() not in (key, 'yes', 'true'):
                del attrs[key]
        elif key.startswith('data_'):
            attrs['data-{0}'.format(key[5:])] = attrs.pop(key)

    return attrs


#
# HTML5 new input types
#
def color(name, **attrs):
    """ Create a color field """

    # Override type attribute
    attrs['type'] = 'color'
    return text(name, **attrs)


def date(name, **attrs):
    """ Create a date field """

    # Override type attribute
    attrs['type'] = 'date'
    return text(name, **attrs)


def datetime_local(name, **attrs):
    """ Create a datetime-local field """

    # Override type attribute
    attrs['type'] = 'datetime-local'
    return text(name, **attrs)


def email(name, **attrs):
    """ Create an email field """

    # Override type attribute
    attrs['type'] = 'email'
    return text(name, **attrs)


def month(name, **attrs):
    """ Create a month field """

    # Override type attribute
    attrs['type'] = 'month'
    return text(name, **attrs)


def number(name, **attrs):
    """ Create a number field """

    # Override type attribute
    attrs['type'] = 'number'
    return text(name, **attrs)


def range(name, **attrs):
    """ Create a range field """

    # Override type attribute
    attrs['type'] = 'range'
    return text(name, **attrs)


def search(name, **attrs):
    """ Create a search field """

    # Override type attribute
    attrs['type'] = 'search'
    return text(name, **attrs)


def tel(name, **attrs):
    """ Create a tel field """

    # Override type attribute
    attrs['type'] = 'tel'
    return text(name, **attrs)


def time(name, **attrs):
    """ Create a time field """

    # Override type attribute
    attrs['type'] = 'time'
    return text(name, **attrs)


def url(name, **attrs):
    """ Create an url field """

    # Override type attribute
    attrs['type'] = 'url'
    return text(name, **attrs)


def week(name, **attrs):
    """ Create a week field """

    # Override type attribute
    attrs['type'] = 'week'
    return text(name, **attrs)
