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

""" API REST interactive documentation view """

from collections import OrderedDict
import importlib
import inspect
import logging
import operator
import os
import re

from formencode.api import NoDefault

from pyramid.path import AssetResolver
from pyramid.renderers import render_to_response
from pyramid.security import NO_PERMISSION_REQUIRED

log = logging.getLogger(__name__)

RE_FUNC_PARAMS = re.compile(r'\((.*?)\)')
RE_LIBRARY_VERSION = re.compile(r"([A-Za-z0-9\.-]+)-(v?[0-9a-f\.]{2,}[0-9a-f]).*")


def datetime_format_python_to_moment(format_):
    """ Convert python datetime format (C Standard 1989) into Moment.js datetime format """

    # year 4 digits
    format_ = format_.replace('%Y', 'YYYY')
    # month 2 digits
    format_ = format_.replace('%m', 'MM')
    # day 2 digits
    format_ = format_.replace('%d', 'DD')
    # hours 2 digits (24h)
    format_ = format_.replace('%H', 'HH')
    # hours 2 digits (12h)
    format_ = format_.replace('%I', 'hh')
    # hours AM/PM
    format_ = format_.replace('%p', 'A')
    # minutes 2 digits
    format_ = format_.replace('%M', 'mm')
    # seconds 2 digits
    format_ = format_.replace('%S', 'ss')

    return format


def inspect_schema_doc(tree, parameters, parent=None):
    """ Inspect `formencode.Schema` documentation """

    if not parameters:
        return

    if isinstance(tree, list):
        for node in tree:
            inspect_schema_doc(node, parameters)
    else:
        if tree[0].__name__ in ('object', 'Declarative') or tree[0].__module__.startswith('formencode'):
            return

        doc = inspect.getdoc(tree[0])
        for line in doc.split('\n'):
            if line.startswith(':param'):
                line = line.split(':', 2)
                if len(line) != 3:
                    continue
                name = line[1].split(' ')[-1].strip()
                if parent is not None:
                    name = '{0}.{1}'.format(parent, name)
                if name in parameters:
                    parameters[name]['description'] = line[2].strip()


def inspect_validator(validator, name=None):
    """ Inspect `formencode.validators.FancyValidator` """

    data = dict(
        description=None,
    )

    if name is not None:
        data['name'] = name
        data['required'] = validator.not_empty is True
        if name in ('format', 'order', 'mode', 'page', 'page_size', 'paging', 'sort'):
            data['parameter_type'] = 'query special'
        else:
            data['parameter_type'] = 'query'

    if_empty = None
    if validator.if_empty is not None and validator.if_empty is not NoDefault:
        if_empty = validator.if_empty
    if_missing = None
    if validator.if_missing is not None and validator.if_missing is not NoDefault:
        if_missing = validator.if_missing
    data['default'] = if_missing or if_empty

    class_name = validator.__class__.__name__
    if class_name.endswith('Validator'):
        class_name = class_name.replace('Validator', '')

    data['type'] = class_name
    if class_name == 'OneOf':
        data['values'] = validator.list
    elif class_name in ('ForEach', 'NumberList', 'StringList'):
        data['items'] = inspect_validator(validator.validators[0]) if validator.validators else None
    elif class_name in ('Int', 'Number'):
        data['min'] = validator.min
        data['max'] = validator.max
    elif data['type'] == 'DateTime':
        if validator.is_date:
            data['type'] = 'Date'
        data['format'] = datetime_format_python_to_moment(validator.format)

    return data


# from CPython project
# https://hg.python.org/cpython/file/tip/Lib/inspect.py
def unwrap(func, stop=None):
    """Get the object wrapped by *func*.

    Follows the chain of :attr:`__wrapped__` attributes returning the last
    object in the chain.

    *stop* is an optional callback accepting an object in the wrapper chain
    as its sole argument that allows the unwrapping to be terminated early if
    the callback returns a true value. If the callback never returns a true
    value, the last object in the chain is returned as usual. For example,
    :func:`signature` uses this to stop unwrapping if any object in the
    chain has a ``__signature__`` attribute defined.

   :exc:`ValueError` is raised if a cycle is encountered.

    """
    if stop is None:
        def _is_wrapper(func):
            return hasattr(func, '__wrapped__')
    else:
        def _is_wrapper(func):
            return hasattr(func, '__wrapped__') and not stop(func)

    # remember the original func for error reporting
    func_ = func

    # Memoise by id to tolerate non-hashable objects
    memo = set([id(func_)])
    while _is_wrapper(func):
        func = func.__wrapped__
        id_func = id(func)
        if id_func in memo:
            raise ValueError('wrapper loop when unwrapping {!r}'.format(func_))
        memo.add(id_func)

    return func


# pylint: disable=too-many-branches,too-many-locals,too-many-statements
def api_doc(request, renderer_values, package):
    """Render API documentation

    Args:
        request (obj): currently active request.
        renderer_values (dict): values passed to renderer.
            breadcrumb: Page breadcrumb
            hide_undocumented: True to hide undocumented services (default False)
            title: Page title
            subtitle: Page subtitle
        package (string): requester package name.

    Returns:
        unicode: HTML response body.

    """

    introspector = request.registry.introspector
    services = OrderedDict()

    for item in introspector.get_category('routes'):
        introspectable = item['introspectable']
        discriminator = introspectable.discriminator

        if not discriminator.startswith('api.'):
            continue

        route_intr = introspector.get('routes', discriminator)
        route = route_intr['object']

        services[discriminator] = dict(
            allowed=True,
            doc=None,
            module=None,
            name=discriminator,
            pattern=request.script_name + route_intr['pattern'],
            parameters=[],
            request_methods=route_intr['request_methods'],
        )

        # get third-party predicates
        thrid_party_predicates = []
        for predicate in route.predicates:
            if predicate.__class__.__name__ == 'EnumPredicate':
                for param, values in predicate.params.items():
                    thrid_party_predicates.append(param)
                    services[discriminator]['parameters'].append(dict(
                        name=param,
                        type='OneOf',
                        parameter_type='path',
                        required=True,
                        default=None,
                        description=None,
                        values=values,
                    ))
            elif predicate.__class__.__name__ == 'NumericPredicate':
                for name in predicate.names:
                    thrid_party_predicates.append(name)
                    services[discriminator]['parameters'].append(dict(
                        name=name,
                        type='Number',
                        parameter_type='path',
                        required=True,
                        default=None,
                        description=None,
                        max=None,
                        min=None,
                    ))

        # get other predicates (not third-party) present in pattern
        for predicate_name in route.match(route_intr['pattern']).keys():
            if predicate_name not in thrid_party_predicates:
                services[discriminator]['parameters'].append(dict(
                    name=predicate_name,
                    type='ByteString',
                    parameter_type='path',
                    required=True,
                    default=None,
                    description=None,
                ))

    for item in introspector.get_category('permissions'):
        introspectable = item['introspectable']
        permission = introspectable.discriminator
        if permission == NO_PERMISSION_REQUIRED:
            continue

        for introspectable_view in item['related']:
            discriminator = introspectable_view['route_name']
            if discriminator in services:
                services[discriminator]['allowed'] = request.has_permission(permission).__class__.__name__ == 'ACLAllowed'

    for item in introspector.get_category('views'):
        introspectable = item['introspectable']
        discriminator = introspectable['route_name']

        if discriminator not in services:
            continue

        if introspectable['request_methods']:
            if isinstance(introspectable['request_methods'], tuple):
                services[discriminator]['request_methods'] = introspectable['request_methods']
            else:
                services[discriminator]['request_methods'] = (introspectable['request_methods'],)

        services[discriminator]['module'] = introspectable['callable'].__venusian_callbacks__['pyramid'][0][1]

        callable_func = unwrap(introspectable['callable'])
        source_lines = inspect.getsourcelines(callable_func)
        for line in source_lines[0]:
            if line.startswith('@validate'):
                parameters = dict()

                schema_name = re.findall(RE_FUNC_PARAMS, line)[0].split(',')[1].strip()
                source_path = inspect.getsourcefile(callable_func)
                with open(source_path, 'r') as fp:
                    for module_line in fp.readlines():
                        if module_line.startswith('from') and schema_name in module_line.split():
                            schema_module_name = module_line.split()[1]
                            break

                schema_module = importlib.import_module(schema_module_name)
                schema = getattr(schema_module, schema_name)

                for name, field in schema.fields.items():
                    class_name = field.__class__.__name__
                    if class_name.endswith('Schema'):
                        for sub_name, sub_field in field.__dict__['fields'].items():
                            parameter_name = '{0}.{1}'.format(name, sub_name)
                            parameters[parameter_name] = inspect_validator(sub_field, parameter_name)

                        inspect_schema_doc((field.__class__,), parameters, name)
                    else:
                        parameters[name] = inspect_validator(field, name)

                inspect_schema_doc(inspect.getclasstree(inspect.getmro(schema), unique=True), parameters)

                # sort parameters by parameter_type and name
                parameters = list(parameters.values())
                parameters.sort(key=operator.itemgetter('parameter_type', 'name'))

                services[discriminator]['parameters'] += parameters
                break

        doc = inspect.getdoc(callable_func)
        if doc is not None:
            doc %= request.registry.settings
        services[discriminator]['doc'] = doc

    modules = OrderedDict()
    orphans = []
    for discriminator, service in services.items():
        if service['module'] is None:
            # service has a route but no view!
            orphans.append(service)
            continue

        if service['module'] not in modules:
            module = importlib.import_module(service['module'])
            modules[service['module']] = dict(
                doc=module.__doc__.strip() if module.__doc__ else None,
                services=[],
            )
        modules[service['module']]['services'].append(service)
    renderer_values['modules'] = modules
    renderer_values['orphans'] = orphans

    # get versions of available JavaScript libraries
    renderer_values['static_lib_versions'] = dict()
    asset_resolver = AssetResolver(package)
    static_lib_path = asset_resolver.resolve('static/lib').abspath()
    for item in os.listdir(static_lib_path):
        matches = RE_LIBRARY_VERSION.findall(item)
        if len(matches) == 1:
            name, version = matches[0]
            renderer_values['static_lib_versions'][name] = version

    renderer_values['package'] = package

    # read CSS and JavaScript code, it must be inlined in HTML page
    bs_major_revision = renderer_values['static_lib_versions']['bootstrap'][0]
    asset_resolver = AssetResolver('pyramid_helpers')
    with open(asset_resolver.resolve('static/css/api-doc-bs{0}.css'.format(bs_major_revision)).abspath(), 'r') as fp:
        renderer_values['css'] = fp.read()
    with open(asset_resolver.resolve('static/js/api-doc-bs{0}.js'.format(bs_major_revision)).abspath(), 'r') as fp:
        renderer_values['js'] = fp.read()

    return render_to_response('/api-doc-bs{0}.mako'.format(bs_major_revision), renderer_values, request, package)
