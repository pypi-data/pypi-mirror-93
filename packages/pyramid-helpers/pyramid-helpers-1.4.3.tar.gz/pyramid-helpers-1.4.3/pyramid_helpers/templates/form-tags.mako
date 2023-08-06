<%!
import json

from pyramid_helpers.forms import tags
from pyramid_helpers.forms.tags import coerce_bool
from pyramid_helpers.forms.tags import html_attrs
%>\
<%doc>

    Mako form tag library.

    Adapts Pylons' webhelpers2.html functions into <%defs> which are readily usable via <%call>.

    The <%call> tags themselves can be more pleasantly used in templates using a
    preprocessor such as process_tags(), which converts XML-style tags into <%call> tags.

</%doc>

<%def name="autocomplete(name, **attrs)">\
<%doc>
    Render an HTML <select> tag.  Options within the tag
    are generated from selected value(s).
</%doc>
<%
    value = form_ctx['current'].value(name) or []
    if isinstance(value, str):
        value = [value]

    attrs['data-value'] = json.dumps(value)
%>\
${tags.select(name, values, options, **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="checkbox(name, value='true', **attrs)">\
<%doc>
    Render an HTML <checkbox> tag.  The value is rendered as 'true'
    by default for usage with the StringBool validator.
</%doc>
<%
    data = form_ctx['current'].value(name)
    if isinstance(data, (list, tuple)):
        checked = str(value) in data
    else:
        checked = str(value) == data
%>\
${tags.checkbox(name, value, checked=checked, **html_attrs(**attrs))}\
${errors(name)}
</%def>

<%def name="color(name, **attrs)">\
<%doc>
    Render an HTML <input type="color"> tag.
</%doc>
${tags.color(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="date(name, **attrs)">\
<%doc>
    Render an HTML <input type="date"> tag.
</%doc>
${tags.date(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="datetime_local(name, **attrs)">\
<%doc>
    Render an HTML <input type="datetime-local"> tag.
</%doc>
${tags.datetime_local(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="email(name, **attrs)">\
<%doc>
    Render an HTML <input type="email"> tag.
</%doc>
${tags.email(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="errors(name, extra_class=None)">\
<%doc>
    Given a field name, produce a stylized error message from the current
    form errors collection, if one is present.  Else render nothing.
</%doc>
<% error = form_ctx['current'].error(name) %>\
% if error:
<div class="alert alert-danger input-error${' {0}'.format(extra_class) if extra_class else ''}">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
    ${error}
</div>
% endif
</%def>

<%def name="form(name, action=None, multipart=False, **attrs)">
<%doc>
    Render an HTML <form> tag - the body contents will be rendered within.

        name - the name of the form stored in request attribute
        action - url to be POSTed to
</%doc>
<%
    # Get form instance
    assert name in forms, 'Invalid form name {0}'.format(name)
    form_ctx['current'] = forms[name]
%>\
${tags.form(action or request.path_qs, multipart=coerce_bool(multipart), name=name, **html_attrs(**attrs))}
% if form_ctx['current'].csrf_token:
    ${tags.hidden('_csrf_token', value=form_ctx['current'].csrf_token)}
% endif
${caller.body()}\
${tags.end_form()}\
<%
    del form_ctx['current']
%>\
</%def>

<%def name="hidden(name, **attrs)">\
<%doc>
    Render an HTML <input type="hidden"> tag.
</%doc>
${tags.hidden(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}
</%def>

<%def name="month(name, **attrs)">\
<%doc>
    Render an HTML <input type="month"> tag.
</%doc>
${tags.month(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="number(name, **attrs)">\
<%doc>
    Render an HTML <input type="number"> tag.
</%doc>
${tags.number(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="optgroup(label)">\
<%doc>
    Render an HTML <optgroup> tag.  This is meant to be used with
    the "select" %def and produces a special return value specific to
    usage with that function.
</%doc>
<%
    options = form_ctx['select_options']

    form_ctx['select_options'] = options.add_optgroup(label)

    capture(caller.body)

    form_ctx['select_options'] = options
%>\
</%def>

<%def name="option(value)">\
<%doc>
    Render an HTML <option> tag.  This is meant to be used with
    the "select" %def and produces a special return value specific to
    usage with that function.
</%doc>
<%
    form_ctx['select_options'].add_option(capture(caller.body).strip(), value=str(value))
%>\
</%def>

<%def name="password(name, **attrs)">\
<%doc>
    Render an HTML <input type="password"> tag.
</%doc>
${tags.password(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="radio(name, value='true', **attrs)">\
<%doc>
    Render an HTML <radio> tag.
</%doc>
<%
    data = form_ctx['current'].value(name)
    if isinstance(data, (list, tuple)):
        checked = str(value) in data
    else:
        checked = str(value) == data
%>\
${tags.radio(name, value, checked=checked, **html_attrs(**attrs))}\
${errors(name)}
</%def>

<%def name="range(name, **attrs)">\
<%doc>
    Render an HTML <input type="range"> tag.
</%doc>
${tags.range(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="select(name, **attrs)">\
<%doc>
    Render an HTML <select> tag.  Options within the tag
    are generated using the "option" %def.
</%doc>
<%
    form_ctx['select_options'] = tags.Options()
    capture(caller.body)
%>\
${tags.select(name, form_ctx['current'].value(name), form_ctx['select_options'], **html_attrs(**attrs))}\
${errors(name)}\
<%
    del form_ctx['select_options']
%>\
</%def>

<%def name="submit(value=None, name=None, **attrs)">\
<%doc>
    Render an HTML <submit> tag.
</%doc>
${tags.submit(name=name, value=value, **html_attrs(**attrs))}\
</%def>

<%def name="tel(name, **attrs)">\
<%doc>
    Render an HTML <input type="tel"> tag.
</%doc>
${tags.tel(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="text(name, **attrs)">\
<%doc>
    Render an HTML <input type="text"> tag.
</%doc>
${tags.text(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="textarea(name, **attrs)">\
<%doc>
    Render an HTML <textarea></textarea> tag pair with embedded content.
</%doc>
${tags.textarea(name, content=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="time(name, **attrs)">\
<%doc>
    Render an HTML <input type="time"> tag.
</%doc>
${tags.time(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="upload(name, **attrs)">\
<%doc>
    Render an HTML <file> tag.
</%doc>
${tags.file(name, **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="url(name, **attrs)">\
<%doc>
    Render an HTML <input type="url"> tag.
</%doc>
${tags.url(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>

<%def name="week(name, **attrs)">\
<%doc>
    Render an HTML <input type="week"> tag.
</%doc>
${tags.week(name, value=form_ctx['current'].value(name), **html_attrs(**attrs))}\
${errors(name)}\
</%def>
