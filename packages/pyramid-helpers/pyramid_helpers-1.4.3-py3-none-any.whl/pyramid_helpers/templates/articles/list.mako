<%namespace name="paginate" file="/paginate.mako"/>
<%
labels = {
    'draft': 'warning',
    'published': 'success',
    'refused': 'danger',
}
pager = request.pagers['articles']
%>\
% if pager.item_count:
    <p>
    % if pager.page_count > 1:
        ${_('article from {0} to {1} on {2}').format(pager.first_item, pager.last_item, pager.item_count)}
    % else:
        ${ungettext('{0} article', '{0} articles', pager.item_count).format(pager.item_count)}
    % endif
        <a class="btn btn-default btn-xs pull-right" href="${request.route_path('articles.search', _query=dict(csv=1))}" title="${_('Download CSV')}"><i class="glyphicon glyphicon-list"> </i></a>
    </p>
        <table class="table">
    % for article in pager:
            <tr>
                <td>
                    <a href="${request.route_path('articles.visual', article=article.id)}" title="${_('View article "{0}"').format(article.title)}">${article.title}</a>
                </td>
        % if has_permission('articles.modify'):
                <td class="text-right">
                    <span class="label label-${labels[article.status]}">${_(article.status.capitalize())}</span>
                    <a class="btn btn-default btn-xs" href="${request.route_path('articles.modify', article=article.id)}" title="${_('Edit article {0}').format(article.title)}"><i class="glyphicon glyphicon-edit"> </i></a>
            % if has_permission('articles.delete'):
                    <a class="btn btn-default btn-xs" href="${request.route_path('articles.delete', article=article.id)}" title="${_('Delete article {0}').format(article.title)}"><i class="glyphicon glyphicon-trash"> </i></a>
            % endif>
                </td>
        % endif
            </tr>
    % endfor
        </table>
        <div class="text-right">
${paginate.render_pages(pager)}
${paginate.render_limit(pager)}
        </div>
% else:
    <div class="alert alert-info">${_('No article.')}</div>
% endif
