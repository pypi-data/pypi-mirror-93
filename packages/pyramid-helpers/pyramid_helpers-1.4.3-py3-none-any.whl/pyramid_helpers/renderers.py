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

""" Custom renderers for Pyramid-Helpers """

import csv
import io
from logging import getLogger

from pyramid.compat import json
from pyramid.httpexceptions import HTTPInternalServerError

log = getLogger(__name__)


# pylint: disable=unused-argument
def csv_renderer_factory(info):
    """ CSV renderer for Pyramid """

    def _render(value, system):
        request = system.get('request')
        _ = request.translate

        # Get parameters
        encoding = value.pop('encoding', 'utf-8')
        filename = value.pop('filename', 'result.csv')
        rows = value.pop('rows', None) or []

        # Create CSV
        try:
            fp = io.StringIO()

            writer = csv.writer(fp, **value)
            writer.writerows(rows)

        except Exception as exc:
            log.exception('Could not convert view response to CSV')
            raise HTTPInternalServerError(explanation=_('Could not convert view response to CSV')) from exc

        # Set content type
        request.response.content_type = 'text/csv; charset="{0}"'.format(encoding)
        request.response.content_disposition = 'attachment; filename="{0}"'.format(filename)

        # Return file content
        fp.seek(0)
        content = fp.read()
        return content.encode(encoding)

    return _render


# pylint: disable=unused-argument
def json_renderer_factory(info):
    """ Custom JSON renderer with callback suppport """

    def _render(value, system):
        request = system.get('request')
        registry = request.registry
        settings = registry.settings

        # Prepare options
        kwargs = dict(
            (k[15:], v)
            for k, v in settings.items()
            if k.startswith('renderers.json.')
        )

        kwargs.pop('enabled')

        if 'indent' in kwargs:
            kwargs['indent'] = int(kwargs['indent'])

        for key in ('skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'sort_keys'):
            if key in kwargs:
                kwargs[key] = kwargs[key].lower() in ('true', 'yes')

        # Extrack callback from query
        callback = kwargs.pop('callback', None)
        if callback:
            callback = request.params.get(callback)

        result = json.dumps(value, default=str, **kwargs)

        if callback:
            request.response.content_type = 'application/javascript; charset="utf-8"'
            result = '{0}({1})'.format(callback, result)
        else:
            request.response.content_type = 'application/json; charset="utf-8"'

        return result

    return _render


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

    config = Configurator()
    config.include('pyramid_helpers.renderers')
    """

    registry = config.registry
    settings = registry.settings

    if settings.get('renderers.csv.enabled', 'false').lower() in ('true', 'yes'):
        # Add CSV renderer
        config.add_renderer('csv', csv_renderer_factory)

    if settings.get('renderers.json.enabled', 'false').lower() in ('true', 'yes'):
        # Replace JSON renderer (callback support)
        config.add_renderer('json', json_renderer_factory)
