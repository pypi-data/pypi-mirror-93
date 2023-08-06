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

""" Pyramid-Helpers resources """

from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Everyone


class Root:
    """ Pyramid-Helpers resources """

    # pylint: disable=too-few-public-methods

    __acl__ = [
        (Allow, Everyone, (
            'articles.search',
            'articles.visual',
        )),

        (Allow, 'group:admin', ALL_PERMISSIONS),

        (Allow, 'group:guest', (
            'articles.create',
            'articles.modify',
        )),
    ]

    def __init__(self, request):
        self.request = request
