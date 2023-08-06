## -*- coding: utf-8 -*-
<%!
import markdown
%>\
<%
missing_libraries = []
for library in ('moment', 'bootstrap-datetimepicker', 'bootstrap-touchspin', 'handlebars'):
    if library not in static_lib_versions:
        missing_libraries.append(library)
%>\
<%inherit file="/site.mako" />
<%def name="head()">
${parent.head()}
    <!-- Moment.js -->
    % if static_lib_versions.get('moment'):
    <script src="${request.static_path('{0}:static/lib/moment-{1}/min/moment.min.js'.format(package, static_lib_versions.get('moment')))}"></script>
        % if localizer.locale_name != 'en':
    <script src="${request.static_path('{0}:static/lib/moment-{1}/locale/{2}.js'.format(package, static_lib_versions.get('moment'), localizer.locale_name))}"></script>
        % endif
    % endif

    <!-- Bootstrap datetimepicker -->
    % if static_lib_versions.get('bootstrap-datetimepicker'):
    <link href="${request.static_path('{0}:static/lib/bootstrap-datetimepicker-{1}/build/css/bootstrap-datetimepicker.min.css'.format(package, static_lib_versions.get('bootstrap-datetimepicker')))}" rel="stylesheet" />
    <script src="${request.static_path('{0}:static/lib/bootstrap-datetimepicker-{1}/build/js/bootstrap-datetimepicker.min.js'.format(package, static_lib_versions.get('bootstrap-datetimepicker')))}"></script>
    % endif

    <!-- Bootstrap TouchSpin -->
    % if static_lib_versions.get('bootstrap-touchspin'):
    <link href="${request.static_path('{0}:static/lib/bootstrap-touchspin-{1}/dist/jquery.bootstrap-touchspin.min.css'.format(package, static_lib_versions.get('bootstrap-touchspin')))}" rel="stylesheet" />
    <script src="${request.static_path('{0}:static/lib/bootstrap-touchspin-{1}/dist/jquery.bootstrap-touchspin.min.js'.format(package, static_lib_versions.get('bootstrap-touchspin')))}"></script>
    % endif

    <!-- Handlebars -->
    <script src="${request.static_path('{0}:static/lib/handlebars-{1}.min.js'.format(package, static_lib_versions.get('handlebars')))}"></script>

    <!-- Custom scripts & CSS -->
    <style>
${css}
    </style>
    <script>
${js | n}
    </script>
</%def>\
\
<%def name="parameter_row(data)">
<%
    id = data['name'].replace('_', '-')

    type_label = '{0} of {1}'.format(data['type'], data['items']['type']) if data['type'] in ('ForEach', 'NumberList', 'StringList',) and data['items'] else data['type']
    if data.get('format') is not None:
        type_label = '{0} <mark> {1} </mark>'.format(type_label, data['format'])
    if data.get('min') is not None and data.get('max') is not None:
        type_label = '{0} <mark> {1} <= x <= {2} </mark>'.format(type_label, data['min'], data['max'])
    elif data.get('min') is not None:
        type_label = '{0} <mark> x >= {1} </mark>'.format(type_label, data['min'])
    elif data.get('max') is not None:
        type_label = '{0} <mark> x <= {1} </mark>'.format(type_label, data['max'])

    required_class = ' form-required danger' if data['required'] else ''
    required_prop = ' required' if data['required'] else ''
%>\
\
<tr class="form-group${required_class}">
    <td><label for="${id}">${data['name']}</label></td>
    <td>
    % if data['type'] in ('Date', 'DateTime'):
        <div class="input-group date ${data['type'].lower()}picker">
            <input type="text" class="form-control input-sm" id="${id}" name="${data['name']}" data-date-format="${data['format']}"${required_prop} />
            <div class="input-group-addon">
                <i class="fa fa-calendar"></i>
            </div>
        </div>
    % elif data['type'] == 'Int':
        <input type="text" class="form-control input-sm touchspin" data-bts-min="${data['min'] or -4294967295}" data-bts-max="${data['max'] or 4294967295}" id="${id}" name="${data['name']}"${required_prop} />
    % elif data['type'] == 'OneOf':
        <select class="form-control input-sm selectpicker no-search" placeholder="--" id="${id}" name="${data['name']}"${required_prop}>
            <option value=""></option>
        % for value in data['values']:
            <option value="${value}">${value}</option>
        % endfor
        </select>
    % elif data['type'] in ('ForEach', 'NumberList', 'StringList',) and data['items'] and data['items']['type'] == 'OneOf':
        <select class="form-control input-sm selectpicker no-search" multiple placeholder="--" id="${id}" name="${data['name']}"${required_prop}>
            <option value=""></option>
        % for value in data['items']['values']:
            <option value="${value}">${value}</option>
        % endfor
        </select>
    % elif data['type'] == 'StringBool':
        <select class="form-control input-sm selectpicker no-search" placeholder="--" id="${id}" name="${data['name']}"${required_prop}>
            <option value=""></option>
            <option value="false">${_('False')}</option>
            <option value="true">${_('True')}</option>
        </select>
    % else:
        <input type="text" class="form-control input-sm" id="${id}" name="${data['name']}"${required_prop} />
    % endif
    </td>
    <td>${data['description'] or '-'}</td>
    <td>${data['parameter_type']}</td>
    <td>${type_label | n}</td>
    <td>${data['default'] if data['default'] not in (None, [], ()) else '-'}</td>
</tr>
</%def>\
\
<div class="row">
    <div class="col-md-6">
        <form class="form-inline">
            <div class="input-group input-group-sm">
                <input class="form-control" type="search" id="input-filter" placeholder="${_('Filter')}" aria-label="${_('Filter')}">
                <div class="input-group-addon">
                    <i class="fas fa-filter"></i>
                </div>
            </div>
        </form>
    </div>

    <div class="col-md-6">
        <button class="btn btn-primary btn-sm pull-right" data-toggle="modal" data-target="#help-modal">
            Help <i class="fa fa-question"></i>
        </button>
        <div class="clearfix"></div>
    </div>
</div>

% if missing_libraries:
<div class="alert alert-warning alert-dismissible">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
    <h4><i class="icon fa fa-ban"></i> ${_('One or more optional libraries are not available!')}</h4>
    <ul>
    % for library in missing_libraries:
        <li>${library}</li>
    % endfor
  </ul>
</div>
% endif

% if orphans:
<div class="alert alert-warning alert-dismissible">
    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
    <h4><i class="icon fa fa-warning"></i> ${_('Orphan routes detected!')}</h4>
    <ul>
    % for service in orphans:
        <li>${' / '.join(service['request_methods'])} ${service['pattern']}</li>
    % endfor
  </ul>
</div>
% endif

% if len(modules):
    % for module_name, module in modules.items():
        <% module_id = 'accordion-module-' + module_name.replace('.', '-') %>
<h4 class="module-title" data-toggle="collapse" data-target="#${module_id}" aria-controls="${module_id}">
    ${module['doc'].split('\n')[0] if module['doc'] is not None else '??? Undocumented module ???'}
    <i class="fa fa-chevron-down pull-right"></i>
</h4>

<div class="panel-group collapse in" id="${module_id}" role="tablist" aria-multiselectable="true">
        % for service in module['services']:
            <% service_id = service['name'].replace('.', '-') %>
            % if not service['allowed'] or (service['doc'] is None and hide_undocumented):
                <% continue %>
            % endif
    <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="heading-${service_id}">
            <h5 class="panel-title service-title" data-toggle="collapse" data-parent="#${module_id}" href="#collapse-${service_id}" aria-expanded="true" aria-controls="collapse-${service_id}">
                ## Methods
            % if service['request_methods']:
                <% method = service['request_methods'][0].lower() %>
                % for request_method in service['request_methods']:
                <span class="label label-lg service-method service-method-${method}">${request_method}</span>
                % endfor
            % else:
                <% method = 'unknown' %>
                <span class="label label-lg service-method service-method-unknown">???</span>
            % endif

                ## Path
                <span class="service-path">
                    ${service['pattern']}
                </span>

            % if service['doc']:
                ## Short description: 1st line of docstring
                <span class="service-description service-description-${method}">
                    ${service['doc'].split('\n')[0]}
                </span>
            % endif
            </h5>
        </div>
        <div id="collapse-${service_id}" class="panel-collapse collapse out" role="tabpanel" aria-labelledby="heading-${service_id}">
            <div class="panel-body service-panel-body-${method}">
            % if service['doc']:
                <div class="alert service-doc-${method}">
                    <label>${service['doc'].split('\n')[0]}</label>
                    <p>${'<br />'.join(service['doc'].split('\n')[1:]) | n}</p>
                </div>
            % endif
                <form action="${service['pattern']}" data-method="${service['request_methods'][0] if service['request_methods'] else ''}">
            % if service['parameters']:
                    <h4>${_('Parameters')}</h4>
                    <table class="table table-condensed table-hover">
                        <thead>
                            <tr>
                                <th>${_('Parameter')}</th>
                                <th>${_('Value')}</th>
                                <th>${_('Description')}</th>
                                <th>${_('Parameter Type')}</th>
                                <th>${_('Data Type')}</th>
                                <th>${_('Default')}</th>
                            </tr>
                        </thead>
                        <tbody>
                % for parameter in service['parameters']:
                            ${parameter_row(parameter)}
                % endfor
                        </tbody>
                    </table>
            % endif
                    <div class="pull-right">
                        <button class="btn btn-primary" type="submit" data-loading-text="<i class='fa fa-circle-o-notch fa-spin'></i> ${_('Send request')}">${_('Send request')}</button>
                    </div>
                </form>
            </div><!-- .panel-body -->
        </div><!-- .panel-collapse -->
    </div><!-- .panel -->
        % endfor
</div><!-- .panel-group -->
    % endfor
% else:
<div class="alert alert-info">${_('No API services found')}</div>
% endif

<!-- Help modal -->
<div class="modal fade" id="help-modal" tabindex="-1" role="dialog" aria-labelledby="help-modal-label">
  <div class="modal-dialog modal-lg" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="help-modal-label">${_('Help')}</h4>
      </div>
      <div class="modal-body">
          <ul class="nav nav-tabs" role="tablist">
              <li role="presentation" class="active"><a href="#request-methods" aria-controls="request-methods" role="tab" data-toggle="tab">Request Methods</a></li>
              <li role="presentation"><a href="#response-codes" aria-controls="response-codes" role="tab" data-toggle="tab">Response Status Codes</a></li>
              <li role="presentation"><a href="#examples" aria-controls="examples" role="tab" data-toggle="tab">Examples</a></li>
              <li role="presentation"><a href="#faq" aria-controls="faq" role="tab" data-toggle="tab">FAQ</a></li>
          </ul>

          <div class="tab-content">
              <!-- Request Methods -->
              <div role="tabpanel" class="tab-pane active" id="request-methods">
                  <table class="table">
                      <tbody>
                          <tr>
                              <td align="right"><span class="label service-method-get">GET</span></td>
                              <td>
                                  <p>The <strong>GET</strong> method is used to **read** (or retrieve) a specific resource (by an identifier) or a collection of resources.</p>

                                  <p>In the “happy” (or non-error) path, <strong>GET</strong> returns a representation in JSON or CSV and an HTTP response code of <mark>200</mark> (OK). In an error case, it most often returns a <mark>404</mark> (NOT FOUND) or <mark>400</mark> (BAD REQUEST).</p>

                                  <p><strong>GET</strong> requests are used only to read data and not change it. Therefore, when used this way, they are considered safe. That is, they can be called without risk of data modification or corruption—calling it once has the same effect as calling it 10 times, or none at all. Additionally, <strong>GET</strong> is idempotent, which means that making multiple identical requests ends up having the same result as a single request.</p>

                                  <p>Parameters must be encoded as a query string (param1=value1&amp;param2=value2&amp;param3=value3...) and append to URL path after a '?'.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="label service-method-post">POST</span></td>
                              <td>
                                  <p>The <strong>POST</strong> method is most-often utilized to **create** new resources.</p>

                                  <p>On successful creation, return HTTP status <mark>201</mark>, returning a Location header with a link to the newly-created resource.</p>

                                  <p><strong>POST</strong> is neither safe nor idempotent. It is therefore recommended for non-idempotent resource requests. Making two identical <strong>POST</strong> requests will most-likely result in two resources containing the same information.</p>

                                  <p>Parameters must be passed in request body.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="label service-method-put">PUT</span></td>
                              <td>
                                  <p>The <strong>PUT</strong> method is used to **update** a specific resource (by an identifier) or a collection of resources.</p>

                                  <p>On successful update, return HTTP status <mark>200</mark> (OK).</p>

                                  <p><strong>PUT</strong> is not a safe operation, in that it modifies state on the server, but it is idempotent. In other words, if you update a resource using <strong>PUT</strong> and then make that same call again, the resource is still there and still has the same state as it did with the first call.</p>

                                  <p>Parameters must be passed in request body.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="label service-method-delete">DELETE</span></td>
                              <td>
                                  <p>The <strong>DELETE</strong> method is pretty easy to understand. It is used to **delete** a resource by an identifier.</p>

                                  <p>On successful deletion, return HTTP status <mark>200</mark> (OK).</p>

                                  <p><strong>DELETE</strong> operations are idempotent. If you <strong>DELETE</strong> a resource, it's removed. Repeatedly calling <strong>DELETE</strong> on that resource ends up the same: the resource is gone.</p>

                                  <p>Parameters must be passed in request body.</p>
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>

              <!-- Response Status Codes -->
              <div role="tabpanel" class="tab-pane" id="response-codes">
                  <table class="table">
                      <tbody>
                          <tr>
                              <th align="right">200</th>
                              <td>OK</td>
                              <td>General success status code. This is the most common code. Used to indicate success.</td>
                          </tr>
                          <tr>
                              <th align="right">201</th>
                              <td>CREATED</td>
                              <td>
                                  Successful creation occurred. Set the Location header to contain a link to the newly-created resource.
                              </td>
                          </tr>
                          <tr>
                              <th align="right">400</th>
                              <td>BAD REQUEST</td>
                              <td>
                                  General error for when fulfilling the request would cause an invalid state. Domain validation errors, missing data, etc. are some examples.
                              </td>
                          </tr>
                          <tr>
                              <th align="right">401</th>
                              <td>UNAUTHORIZED</td>
                              <td>
                                  Error code response for missing or invalid authentication token.
                              </td>
                          </tr>
                          <tr>
                              <th align="right">403</th>
                              <td>FORBIDDEN</td>
                              <td>
                                  Error code for when the user is not authorized to perform the operation or the resource is unavailable for some reason (e.g. time constraints, etc.).
                              </td>
                          </tr>
                          <tr>
                              <th align="right">404</th>
                              <td>NOT FOUND</td>
                              <td>
                                  Used when the requested resource is not found, whether it doesn't exist or if there was a <mark>401</mark> or <mark>403</mark> that, for security reasons, the service wants to mask.
                              </td>
                          </tr>
                          <tr>
                              <th align="right">500</th>
                              <td>INTERNAL SERVER ERROR</td>
                              <td>
                                  The general catch-all error when the server-side throws an exception.
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </div>

              <!-- Examples -->
              <div role="tabpanel" class="tab-pane" id="examples">
<%
content = _('No examples found')
md_path = request.registry.settings.get('api_doc.examples_md_file')
if md_path:
    with open(md_path, 'r') as f:
        content = f.read()
%>
${markdown.markdown(content, extensions=['markdown.extensions.codehilite']) | n}
              </div>

              <!-- FAQ -->
              <div role="tabpanel" class="tab-pane" id="faq">
                  <h3>What is paging and how does it work?</h3>
                  <p>Paging is the process of dividing a response into several pages.</p>
                  <p>Sometime, a call to an API services returns a massive number of results. In this case, paging is useful for a better handling of the response.</p>

                  <h4>Paging parameters in request</h4>
                  <dl class="dl-horizontal">
                      <dt>paging</dt>
                      <dd>True value enables paging.</dd>
                      <dt>page_size</dt>
                      <dd>Allows you to define the number of items that will be returned in each page.</dd>
                      <dt>page</dt>
                      <dd>Allows you to define the numero of the desired page.</dd>
                      <dd><em>If it's greater than number of pages, no data will be returned.</em></dd>
                  </dl>

                  <h4>Paging information in response</h4>
                  <dl class="dl-horizontal">
                      <dt>pageSize</dt>
                      <dd>Number of items requested by page</dd>
                      <dt>page</dt>
                      <dd>Numero of the current page</dd>
                      <dt>pageItemCount</dt>
                      <dd>Number of items in current page (equal or inferior to pageSize)</dd>
                      <dt>totalItemCount</dt>
                      <dd>Total number of items (all pages combined)</dd>
                      <dt>pageStartIndex</dt>
                      <dd>Index of the first item</dd>
                  </dl>
              </div>
          </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">${_('Close')}</button>
      </div>
    </div>
  </div>
</div>

<!-- Response modal -->
<div class="modal fade" id="response-modal" tabindex="-1" role="dialog" aria-labelledby="response-modal-label">
  <div class="modal-dialog modal-lg" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="response-modal-label">${_('Response')}</h4>
      </div>
      <div class="modal-body">
          <div id="response-request-url">
              <h4>${_('Request URL')}</h4>
              <pre></pre>
          </div>
          <div id="response-request-data">
              <h4>${_('Request Data')}</h4>
              <pre></pre>
          </div>
          <div id="response-request-curl-cmd">
              <h4>${_('CURL Command')}</h4>
              <pre></pre>
          </div>
          <div id="response-code">
              <h4>${_('Response Status Code')}</h4>
              <pre></pre>
          </div>
          <div id="response-body">
              <h4>${_('Response Body')}</h4>
              <pre></pre>
          </div>
          <div id="response-headers">
              <h4>${_('Response Headers')}</h4>
              <pre></pre>
          </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">${_('Close')}</button>
      </div>
    </div>
  </div>
</div>

<script id="form-error" type="text/x-handlebars-template">
  <div class="alert alert-danger input-error">
      <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
      {{message}}
  </div>
</script>
