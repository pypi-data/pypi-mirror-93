# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyramid_helpers',
 'pyramid_helpers.forms',
 'pyramid_helpers.funcs',
 'pyramid_helpers.models',
 'pyramid_helpers.scripts',
 'pyramid_helpers.views',
 'pyramid_helpers.views.api']

package_data = \
{'': ['*'],
 'pyramid_helpers': ['static/css/*',
                     'static/js/*',
                     'static/lib/*',
                     'static/lib/bootstrap-3.3.2-dist/css/*',
                     'static/lib/bootstrap-3.3.2-dist/fonts/*',
                     'static/lib/bootstrap-3.3.2-dist/js/*',
                     'templates/*',
                     'templates/articles/*']}

install_requires = \
['babel>=2.9,<3.0',
 'colorlog>=4.6,<5.0',
 'decorator>=4.4,<5.0',
 'formencode>=2.0.0a1+987d2992,<3.0.0',
 'mako>=1.1,<2.0',
 'passlib>=1.7,<2.0',
 'pyramid-beaker>=0.8,<0.9',
 'pyramid-exclog>=1.0,<2.0',
 'pyramid-mako>=1.1,<2.0',
 'pyramid-tm>=2.4,<3.0',
 'pyramid<1.99',
 'pytz',
 'sqlalchemy>=1.3,<2.0',
 'transaction>=3.0,<4.0',
 'webhelpers2>=2.0,<3.0',
 'zope.sqlalchemy>=1.3,<2.0']

extras_require = \
{'api-doc': ['markdown>=3.3,<4.0'],
 'auth-ldap': ['python-ldap>=3.3,<4.0'],
 'auth-radius': ['pyrad>=2.3,<3.0'],
 'binary': ['psycopg2-binary>=2.8,<3.0'],
 'source': ['psycopg2>=2.8,<3.0']}

entry_points = \
{'console_scripts': ['phelpers-init-db = '
                     'pyramid_helpers.scripts.initializedb:main'],
 'paste.app_factory': ['main = pyramid_helpers:main']}

setup_kwargs = {
    'name': 'pyramid-helpers',
    'version': '1.4.3',
    'description': 'Helpers to develop Pyramid applications',
    'long_description': '# Pyramid-Helpers\n\nPyramid-Helpers is a set of helpers to develop applications using Pyramid framework.\n\nIt includes authentication, forms, i18n and pagination helpers.\n\n\n## Prerequisites\nThe project is managed using [Poetry](https://poetry.eustace.io/docs/#installation)\n\n### PostgreSQL adapter (Optional)\nIn order to use a PostgreSQL database, it is recommended to install the [psycopg](https://www.psycopg.org/) adapter. You should check the [build prerequisites](https://www.psycopg.org/docs/install.html#build-prerequisites) in order to install this package (source only).\n\n### LDAP client (Optional)\nLDAP client relies on the [python-ldap](https://www.python-ldap.org/en/latest/) client. You should check the [build prerequisites](https://www.python-ldap.org/en/latest/installing.html#build-prerequisites) in order to install this package.\n\n\n## Development\n```\n# Create virtualenv\nmkdir .venv\npython3 -m venv .venv\n\n# Activate virtualenv\nsource .venv/bin/activate\n\n# Update virtualenv\npip install -U pip setuptools\n\n# Install Poetry\npip install wheel\npip install poetry\n\n# Install application in development mode\npoetry install --extras "{source|binary} [api-doc] [auth-ldap] [auth-radius]"\npoetry run invoke i18n.generate\n\n# Copy and adapt conf/ directory\ncp -a conf .conf\n\n# Initialize database\nphelpers-init-db .conf/application.ini\n\n# Run web server in development mode\npoetry run invoke service.httpd --config-uri=.conf/application.ini --env=.conf/environment\n\n# Run static and functional tests:\npoetry run invoke test --config-uri=.conf/application.ini --env=.conf/environment\n```\n\n## I18n\nExtract messages\n```\npoetry run invoke i18n.extract i18n.update\n```\n\nCompile catalogs and update JSON files\n```\npoetry run invoke i18n.generate\n```\n\nCreate new language\n```\npoetry run invoke i18n.init {locale_name}\n```\n\n\n## Installation\n\n```\npip install pyramid-helpers\n\n# And optionally:\nphelpers-init-db conf/application.ini\n```\n\n\n## Files list\n\n```\n.\n├── babel.cfg                           Babel configuration file (i18n)\n├── CHANGES.md\n├── pylintrc                            Pylint configuration file\n├── pyproject.toml                      Poetry configuration file\n├── README.md\n├── setup.cfg\n├── pyramid_helpers\n│\xa0\xa0 ├── __init__.py                     demo app config\n│\xa0\xa0 ├── auth.py                         auth helpers for demo app\n│\xa0\xa0 ├── models.py                       SQLAlchemy model for demo app\n│\xa0\xa0 ├── paginate.py                     pagination class, decorator and setup\n│\xa0\xa0 ├── predicates.py                   custom route predicates (Enum, Numeric)\n│\xa0\xa0 ├── resources.py                    basic resource file for demo app\n│\xa0\xa0 ├── conf\n│\xa0\xa0 │\xa0\xa0 ├── application.ini             Main configuration file\n│\xa0\xa0 │\xa0\xa0 ├── auth.ini                    Authentication configuration\n│\xa0\xa0 │\xa0\xa0 ├── ldap.ini                    LDAP configuration file (auth)\n│\xa0\xa0 │\xa0\xa0 └── radius.ini                  RADIUS configuration file (auth)\n│\xa0\xa0 ├── forms\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py                 form class, decorator and setup, largely inspired from formhelpers[1]\n│\xa0\xa0 │\xa0\xa0 ├── auth.py                     formencode schema for authentication for demo app\n│\xa0\xa0 │\xa0\xa0 ├── articles.py                 formencode schemas for articles for demo app\n│\xa0\xa0 │\xa0\xa0 ├── tags.py                     HTML input tags renderers\n│\xa0\xa0 │\xa0\xa0 └── validators.py               various formencode validators\n│\xa0\xa0 ├── funcs\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py\n│\xa0\xa0 │\xa0\xa0 └── articles.py                 functions for articles management\n│\xa0\xa0 ├── i18n.py                         i18n setup and helpers\n│\xa0\xa0 ├── locale\n│\xa0\xa0 │\xa0\xa0 ├── fr\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── LC_MESSAGES\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0     └── pyramid-helpers.po\n│\xa0\xa0 │\xa0\xa0 └── pyramid-helpers.pot\n│\xa0\xa0 ├── scripts\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py\n│\xa0\xa0 │\xa0\xa0 └── initializedb.py\n│\xa0\xa0 ├── static\n│\xa0\xa0 │\xa0\xa0 ├── css\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── pyramid-helpers.css     demo app stylesheet\n│\xa0\xa0 │\xa0\xa0 └── js\n│\xa0\xa0 │\xa0\xa0  \xa0\xa0 └── pyramid-helpers.js      demo app javascript\n│\xa0\xa0 ├── templates                       Mako templates\n│\xa0\xa0 │\xa0\xa0 ├── articles                    Mako templates for demo app\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 ├── edit.mako\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 ├── index.mako\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── view.mako\n│\xa0\xa0 │\xa0\xa0 ├── confirm.mako\n│\xa0\xa0 │\xa0\xa0 ├── errors.mako\n│\xa0\xa0 │\xa0\xa0 ├── form-tags.mako              Mako templates for forms rendering - derivates from formhelpers[1]\n│\xa0\xa0 │\xa0\xa0 ├── login.mako\n│\xa0\xa0 │\xa0\xa0 ├── paginate.mako               Mako templates for pagination rendering\n│\xa0\xa0 │\xa0\xa0 ├── site.mako                   Main template\n│\xa0\xa0 │\xa0\xa0 └── validators.mako             Test template for validators\n│\xa0\xa0 └── views\n│\xa0\xa0     ├── __init__.py\n│\xa0\xa0     └── articles.py\n├── tasks                               Invoke tasks\n│ \xa0 ├── __init__.py                     initialization\n│ \xa0 ├── common.py                       common file\n│ \xa0 ├── i18n.py                         i18n tasks\n│ \xa0 ├── service.py                      service tasks\n│ \xa0 └── test.py                         test tasks\n└── tests                               Functional tests (pytest)\n    ├── api\n    │\xa0\xa0 └── test_articles.py            test functions for articles API\n    ├── conftest.py                     configuration file for pytest\n    └── test_validators.py              test functions for formencode validators\n```\n\n\n## Useful documentation\n\n* https://docs.pylonsproject.org/projects/pyramid/en/latest/\n* https://docs.pylonsproject.org/projects/pyramid/en/latest/#api-documentation\n* https://techspot.zzzeek.org/2008/07/01/better-form-generation-with-mako-and-pylons/\n',
    'author': 'Cyril Lacoux',
    'author_email': 'clacoux@easter-eggs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yack/pyramid-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
