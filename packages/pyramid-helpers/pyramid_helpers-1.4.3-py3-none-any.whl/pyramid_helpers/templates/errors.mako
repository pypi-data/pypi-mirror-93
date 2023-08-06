<%inherit file="/site.mako" />\
<div class="alert alert-danger">
    <strong>${_('Error:')}</strong> ${_(request.exception.explanation)}
% if request.exception.code == 403 and request.authenticated_user is None:
    <br />
    <% login_link = '<a href="{0}" class="alert-link">{1}</a>'.format(request.route_path('login'), _('login[action]')) %>
    ${_('Authentication is required to access this resource, please {0} in order to proceed.').format(login_link) | n}
% endif
</div>
