<%def name="render_limit(pager, extra_class=None)">
<ul class="nav ph-limit mr-2 pagination${' {0}'.format(extra_class) if extra_class else ''}">
% for limit in pager.limits:
    <li class="page-item${' active' if limit == pager.limit else ''}">
        <a class="page-link partial-link" href="${pager.link(limit=limit)}" title="${_('View {0} items per page').format(limit)}">${limit}</a>
    </li>
% endfor
</ul>
</%def>

<%def name="render_pages(pager, extra_class=None)">
% if pager.page_count > 1:
<ul class="nav ph-pages pagination${' {0}'.format(extra_class) if extra_class else ''}">
    <li class="page-item${' disabled' if pager.page == 1 else ''}">
        <a class="page-link partial-link" href="${pager.link(page=pager.page - 1)}"><i class="fa fa-chevron-left"> </i></a>
    </li>
    <% links = pager.links(2, 2) %>
    % if links[0][0] != 1:
    <li class="page-item"><a class="page-link partial-link item" href="${pager.link(page=1)}">1</a></li>
    <li class="page-item"><span class="page-link">...</span></li>
    % endif
    % for (page, url) in links:
    <li class="page-item${' active' if pager.page == page else ''}"><a class="page-link partial-link" href="${url}">${page}</a></li>
    % endfor
    % if links[-1][0] != pager.last_page:
    <li class="page-item"><span class="page-link">...</span></li>
    <li class="page-item"><a class="page-link partial-link item" href="${pager.link(page=pager.last_page)}">${pager.last_page}</a></li>
    % endif
    <li class="page-item${' disabled' if pager.page == pager.last_page else ''}">
        <a class="page-link partial-link" href="${pager.link(page=pager.page + 1)}"><i class="fa fa-chevron-right"> </i></a>
    </li>
</ul>
% endif
</%def>
