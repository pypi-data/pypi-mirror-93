<%inherit file="/site.mako" />\
<div class="alert alert-info">
    <h4 class="alert-heading">${_('You have been successfuly logged out!')}</h4>
    ${_('You may return to <a href="{0}" class="alert-link">home page</a>.').format(request.route_path('index')) | n}
</div>
