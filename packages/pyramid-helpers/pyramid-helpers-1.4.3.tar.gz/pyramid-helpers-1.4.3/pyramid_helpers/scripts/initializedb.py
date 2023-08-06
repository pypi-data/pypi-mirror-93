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


""" Database initialization script """

from argparse import ArgumentParser
import sys
import transaction

from pyramid.config import Configurator
from pyramid.paster import get_appsettings
from pyramid.paster import setup_logging

from pyramid_helpers.models import Base
from pyramid_helpers.models import DBSession
from pyramid_helpers.models.articles import Article
from pyramid_helpers.models.core import Group
from pyramid_helpers.models.core import User
from pyramid_helpers.utils import random_string


def main(argv=None):
    """ Database initialization """

    if argv is None:
        argv = sys.argv[1:]

    parser = ArgumentParser(description='Database initialization script')

    parser.add_argument(
        'config_uri',
        help='Configuration file to use.'
    )

    args = parser.parse_args(argv)

    setup_logging(args.config_uri)

    try:
        # Production
        settings = get_appsettings(args.config_uri, name='genconf')
    except LookupError:
        # Development
        settings = get_appsettings(args.config_uri)

    config = Configurator(settings=settings)

    # Model setup
    config.include('pyramid_helpers.models')

    Base.metadata.create_all()

    # Populate table users
    with transaction.manager:
        for name in ['admin', 'guest']:
            group = DBSession.query(Group).filter(Group.name == name).first()
            if group is None:
                group = Group()
                DBSession.add(group)

            group.from_dict(dict(
                name=name,
                description=f'{name} group description',
            ))

            user = DBSession.query(User).filter(User.username == name).first()
            if user is None:
                user = User()
                DBSession.add(user)

            user.from_dict(dict(
                groups=[group],
                password=name,
                status='active',
                token=random_string(40),
                username=name,
            ))

    # Flush table articles
    with transaction.manager:
        DBSession.query(Article).delete()

    # Populate table articles
    with transaction.manager:
        author = DBSession.query(User).filter(User.username == 'admin').first()

        for i in range(1, 100):
            article = Article()
            DBSession.add(article)

            article.from_dict(dict(
                author=author,
                title=f'Article #{i}',
                text=f'Text of article #{i}',
                status='published',
            ))
