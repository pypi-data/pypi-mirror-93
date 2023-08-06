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
Articles API
"""

from pyramid.view import view_config

from pyramid_helpers.forms import validate
from pyramid_helpers.forms.articles import CreateForm
from pyramid_helpers.forms.articles import SearchForm
from pyramid_helpers.forms.articles import StatusForm
from pyramid_helpers.funcs.articles import build_search_query
from pyramid_helpers.funcs.articles import create_or_modify
from pyramid_helpers.funcs.articles import get_article
from pyramid_helpers.models import DBSession
from pyramid_helpers.paginate import paginate


@view_config(route_name='api.articles.create', renderer='json', permission='articles.create')
@validate('article', CreateForm)
def create(request):
    """
    Creates an article
    """
    _ = request.translate
    form = request.forms['article']

    result = dict(
        method=request.path,
        apiVersion='1.0',
        params=form.params,
        result=True,
    )

    article = create_or_modify(request, form)
    if article is None:
        result['message'] = _('Missing or invalid parameter(s)')
        result['result'] = False
        result['errors'] = form.errors
        request.response.status_int = 400

        return result

    result['article'] = article.to_json()
    request.response.status_int = 201

    return result


@view_config(route_name='api.articles.delete', renderer='json', permission='articles.delete')
def delete(request):
    """
    Deletes an article
    """
    _ = request.translate

    result = dict(
        method=request.path,
        apiVersion='1.0',
        result=True,
    )

    article = get_article(request)
    if article is None:
        result['message'] = _('Invalid article')
        result['result'] = False
        request.response.status_int = 404

        return result

    DBSession.delete(article)

    return result


@view_config(route_name='api.articles.modify', renderer='json', permission='articles.modify')
@validate('article', CreateForm)
def modify(request):
    """
    Modifies an article
    """
    _ = request.translate
    form = request.forms['article']

    result = dict(
        method=request.path,
        apiVersion='1.0',
        params=form.params,
        result=True,
    )

    article = get_article(request)
    if article is None:
        result['message'] = _('Invalid article')
        result['result'] = False
        request.response.status_int = 404

        return result

    if not create_or_modify(request, form, article=article):
        result['message'] = _('Missing or invalid parameter(s)')
        result['result'] = False
        result['errors'] = form.errors
        request.response.status_int = 400

        return result

    result['article'] = article.to_json()

    return result


@view_config(route_name='api.articles.status', renderer='json', permission='articles.modify')
@validate('status', StatusForm)
def status(request):
    """
    Changes an article status
    """
    _ = request.translate
    form = request.forms['status']

    result = dict(
        method=request.path,
        apiVersion='1.0',
        params=form.params,
        result=True,
    )

    article = get_article(request)
    if article is None:
        result['message'] = _('Invalid article')
        result['result'] = False
        request.response.status_int = 404

        return result

    if form.errors:
        result['result'] = False
        result['errors'] = form.errors
        request.response.status_int = 400

        return result

    # Update object
    article.from_dict(form.result)

    result['article'] = article.to_json()

    return result


@view_config(route_name='api.articles.search', renderer='json', permission='articles.search')
@paginate('articles', limit=10, sort='id', order='desc')
@validate('search', SearchForm, method='get')
def search(request):
    """
    Searches in articles
    """
    form = request.forms['search']
    pager = request.pagers['articles']

    result = dict(
        method=request.path,
        apiVersion='1.0',
        params=form.params,
        result=True,
    )

    if form.errors:
        result['result'] = False
        result['errors'] = form.errors
        request.response.status_int = 400

        return result

    query = build_search_query(order=pager.order, sort=pager.sort, **form.result)
    pager.set_collection(query)

    result['articles'] = dict(
        items=[article.to_json(context='api.search') for article in pager],
        pager=dict(
            limit=pager.limit,
            page=pager.page,
            pages=pager.page_count,
            total=pager.item_count,
        )
    )

    return result


@view_config(route_name='api.articles.visual', renderer='json', permission='articles.visual')
def visual(request):
    """
    Gets an article
    """
    _ = request.translate

    result = dict(
        method=request.path,
        apiVersion='1.0',
        result=True,
    )

    article = get_article(request)
    if article is None:
        result['message'] = _('Invalid article')
        result['result'] = False
        request.response.status_int = 404

        return result

    result['article'] = article.to_json()

    return result
