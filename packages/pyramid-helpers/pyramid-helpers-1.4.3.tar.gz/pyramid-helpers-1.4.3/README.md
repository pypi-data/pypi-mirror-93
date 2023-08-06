# Pyramid-Helpers

Pyramid-Helpers is a set of helpers to develop applications using Pyramid framework.

It includes authentication, forms, i18n and pagination helpers.


## Prerequisites
The project is managed using [Poetry](https://poetry.eustace.io/docs/#installation)

### PostgreSQL adapter (Optional)
In order to use a PostgreSQL database, it is recommended to install the [psycopg](https://www.psycopg.org/) adapter. You should check the [build prerequisites](https://www.psycopg.org/docs/install.html#build-prerequisites) in order to install this package (source only).

### LDAP client (Optional)
LDAP client relies on the [python-ldap](https://www.python-ldap.org/en/latest/) client. You should check the [build prerequisites](https://www.python-ldap.org/en/latest/installing.html#build-prerequisites) in order to install this package.


## Development
```
# Create virtualenv
mkdir .venv
python3 -m venv .venv

# Activate virtualenv
source .venv/bin/activate

# Update virtualenv
pip install -U pip setuptools

# Install Poetry
pip install wheel
pip install poetry

# Install application in development mode
poetry install --extras "{source|binary} [api-doc] [auth-ldap] [auth-radius]"
poetry run invoke i18n.generate

# Copy and adapt conf/ directory
cp -a conf .conf

# Initialize database
phelpers-init-db .conf/application.ini

# Run web server in development mode
poetry run invoke service.httpd --config-uri=.conf/application.ini --env=.conf/environment

# Run static and functional tests:
poetry run invoke test --config-uri=.conf/application.ini --env=.conf/environment
```

## I18n
Extract messages
```
poetry run invoke i18n.extract i18n.update
```

Compile catalogs and update JSON files
```
poetry run invoke i18n.generate
```

Create new language
```
poetry run invoke i18n.init {locale_name}
```


## Installation

```
pip install pyramid-helpers

# And optionally:
phelpers-init-db conf/application.ini
```


## Files list

```
.
├── babel.cfg                           Babel configuration file (i18n)
├── CHANGES.md
├── pylintrc                            Pylint configuration file
├── pyproject.toml                      Poetry configuration file
├── README.md
├── setup.cfg
├── pyramid_helpers
│   ├── __init__.py                     demo app config
│   ├── auth.py                         auth helpers for demo app
│   ├── models.py                       SQLAlchemy model for demo app
│   ├── paginate.py                     pagination class, decorator and setup
│   ├── predicates.py                   custom route predicates (Enum, Numeric)
│   ├── resources.py                    basic resource file for demo app
│   ├── conf
│   │   ├── application.ini             Main configuration file
│   │   ├── auth.ini                    Authentication configuration
│   │   ├── ldap.ini                    LDAP configuration file (auth)
│   │   └── radius.ini                  RADIUS configuration file (auth)
│   ├── forms
│   │   ├── __init__.py                 form class, decorator and setup, largely inspired from formhelpers[1]
│   │   ├── auth.py                     formencode schema for authentication for demo app
│   │   ├── articles.py                 formencode schemas for articles for demo app
│   │   ├── tags.py                     HTML input tags renderers
│   │   └── validators.py               various formencode validators
│   ├── funcs
│   │   ├── __init__.py
│   │   └── articles.py                 functions for articles management
│   ├── i18n.py                         i18n setup and helpers
│   ├── locale
│   │   ├── fr
│   │   │   └── LC_MESSAGES
│   │   │       └── pyramid-helpers.po
│   │   └── pyramid-helpers.pot
│   ├── scripts
│   │   ├── __init__.py
│   │   └── initializedb.py
│   ├── static
│   │   ├── css
│   │   │   └── pyramid-helpers.css     demo app stylesheet
│   │   └── js
│   │       └── pyramid-helpers.js      demo app javascript
│   ├── templates                       Mako templates
│   │   ├── articles                    Mako templates for demo app
│   │   │   ├── edit.mako
│   │   │   ├── index.mako
│   │   │   └── view.mako
│   │   ├── confirm.mako
│   │   ├── errors.mako
│   │   ├── form-tags.mako              Mako templates for forms rendering - derivates from formhelpers[1]
│   │   ├── login.mako
│   │   ├── paginate.mako               Mako templates for pagination rendering
│   │   ├── site.mako                   Main template
│   │   └── validators.mako             Test template for validators
│   └── views
│       ├── __init__.py
│       └── articles.py
├── tasks                               Invoke tasks
│   ├── __init__.py                     initialization
│   ├── common.py                       common file
│   ├── i18n.py                         i18n tasks
│   ├── service.py                      service tasks
│   └── test.py                         test tasks
└── tests                               Functional tests (pytest)
    ├── api
    │   └── test_articles.py            test functions for articles API
    ├── conftest.py                     configuration file for pytest
    └── test_validators.py              test functions for formencode validators
```


## Useful documentation

* https://docs.pylonsproject.org/projects/pyramid/en/latest/
* https://docs.pylonsproject.org/projects/pyramid/en/latest/#api-documentation
* https://techspot.zzzeek.org/2008/07/01/better-form-generation-with-mako-and-pylons/
