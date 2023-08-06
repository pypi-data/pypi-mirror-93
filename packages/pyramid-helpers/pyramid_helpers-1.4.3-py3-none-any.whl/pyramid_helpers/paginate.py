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


""" Pagination helpers for Pyramid """

from decorator import decorator
from pyramid.decorator import reify
from pyramid.request import Request


LIMITS = (10, 20, 30, 50)


class Pager(list):
    """ Pagination class """

    # pylint: disable=too-many-instance-attributes

    # pylint: disable=too-many-arguments
    def __init__(self, request, name, form=None, limit=10, limits=None, sort=None, order=None, volatile_items=(), **url_kwargs):

        # Calling inherited
        super().__init__()

        self.name = name
        self.request = request
        self.defaults = dict(
            limit=limit,
            sort=sort,
            order=order,
        )

        # Keys
        self.form_key = form
        self.limit_key = '{0}.limit'.format(name)
        self.order_key = '{0}.order'.format(name)
        self.page_key = '{0}.page'.format(name)
        self.partial_key = '{0}.partial'.format(name)
        self.sort_key = '{0}.sort'.format(name)
        self.volatile_items = volatile_items + (self.page_key, self.partial_key)

        # Empty list
        self.item_count = 0
        self.page_count = 0
        self.first_page = None
        self.last_page = None

        self.first_item = None
        self.last_item = None
        self.__page = None

        self.url_kwargs = url_kwargs

        if limits is None:
            registry = request.registry
            settings = registry.settings
            limits = settings['pagers.limits']

        self.limits = limits

    @reify
    def form(self):
        """ Associated form object """

        if self.form_key is None:
            return None

        return self.request.forms.get(self.form_key)

    @reify
    def limit(self):
        """ Limit parameter """

        limit = self.request.params.get(self.limit_key)

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = self.request.session.get(self.limit_key, self.defaults['limit'])

        return limit

    @reify
    def order(self):
        """ Order parameter """

        return self.request.params.get(self.order_key, self.defaults['order'])

    @property
    def page(self):
        """ Page parameter """

        if self.__page is not None:
            return self.__page

        page = self.request.params.get(self.page_key)

        try:
            page = int(page)
        except (TypeError, ValueError):
            if self.form is not None and self.form.submitted:
                # Got to first page if associated form has been submitted
                page = 1
            else:
                page = self.request.session.get(self.page_key, 1)

        self.__page = page
        return page

    @reify
    def params(self):
        """ Query parameters """

        all_params = self.request.params.mixed()

        params = dict(
            (k, v)
            for k, v in all_params.items()
            if k not in self.volatile_items
        )
        return params

    @reify
    def partial(self):
        """ Partial parameter """

        return self.partial_key in self.request.params

    @reify
    def sort(self):
        """ Sort parameter """

        return self.request.params.get(self.sort_key, self.defaults['sort'])

    def header_class(self, key):
        """ Get header class for key """

        if self.sort == key:
            extra = 'fa-sort-up' if self.order == 'desc' else 'fa-sort-down'
        else:
            extra = 'fa-sort'
        return 'fa {0}'.format(extra)

    def link(self, page=1, limit=None, sort=None, order=None):
        """ Compute a pagination link """

        params = self.params.copy()
        if page == -1:
            page = self.last_page
        params[self.page_key] = page
        if limit:
            params[self.limit_key] = limit
        if sort:
            params[self.sort_key] = sort
        if order:
            if order == 'toggle':
                if self.sort == sort:
                    order = 'asc' if self.order == 'desc' else 'desc'
                else:
                    order = 'asc'
            params[self.order_key] = order
        return self.request.current_route_path(_query=params, **self.url_kwargs)

    def links(self, before=3, after=3):
        """ Compute pagination links """

        links = []
        for page in range(self.page - before, self.page + after + 1):
            if page < self.first_page or page > self.last_page:
                continue
            links.append((page, self.link(page=page)))
        return links

    def set_collection(self, collection):
        """ Set collection to pager """

        # Clear
        del self[:]

        try:
            # SQLAlchemy: reset order by clause to speed up query
            self.item_count = collection.order_by(None).count()
        except AttributeError:
            # Regular list
            self.item_count = len(collection)

        if self.item_count:
            self.page_count = ((self.item_count - 1) // self.limit) + 1
            self.first_page = 1
            self.last_page = self.page_count

            if self.page < self.first_page:
                self.__page = self.first_page
            elif self.page > self.last_page:
                self.__page = self.last_page

            self.first_item = (self.page - 1) * self.limit + 1
            self.last_item = min(self.first_item + self.limit - 1, self.item_count)

            items = collection[self.first_item - 1:self.last_item]
            self.extend(items)

        self.request.session[self.page_key] = self.page
        self.request.session[self.limit_key] = self.limit


def on_before_renderer(event):
    """ Add pagers and pager_ctx dictionnaries to renderer context """
    request = event['request']
    event['pagers'] = request.pagers
    event['pager_ctx'] = request.pager_ctx


def on_new_request(event):
    """
    Add pagers and pager_ctx dictionnaries to request

    pagers dictionnary will carry all pagers object using pager's name as key
    pager_ctx dictionnary will carry current pager context:
        'current' key is reserved for current pager object
    """
    request = event.request
    request.pagers = {}
    request.pager_ctx = {}


def paginate(name, partial_template=None, **pager_kwargs):
    """ Pagination decorator """

    def wrapper(func, *args, **kwargs):

        # Get request object from args
        # First arg is «self» when func is method
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break

        if request is None:
            raise ValueError('Missing request object in args list when calling @paginate')

        # Initialize pager object
        pager = Pager(request, name, **pager_kwargs)

        # Store the pager
        request.pagers[name] = pager

        # Call function
        result = func(*args, **kwargs)

        if not request.is_response(result) and pager.partial and partial_template:
            # Override template if needed
            request.override_renderer = partial_template

        return result

    return decorator(wrapper)


def includeme(config):
    """
    Set up standard configurator registrations. Use via:

    .. code-block:: python

    config = Configurator()
    config.include('pyramid_helpers.paginate')
    """

    registry = config.registry
    settings = registry.settings

    if settings.get('pagers.enabled', 'false').lower() not in ('true', 'yes'):
        return

    try:
        limits = list(map(int, settings['pagers.limits'].split()))
        # Add default value if missing
        if 10 not in limits:
            limits.append(10)
        limits.sort()
    except (KeyError, ValueError):
        limits = LIMITS

    settings['pagers.limits'] = limits

    config.add_subscriber(on_before_renderer, 'pyramid.events.BeforeRender')
    config.add_subscriber(on_new_request, 'pyramid.events.NewRequest')
