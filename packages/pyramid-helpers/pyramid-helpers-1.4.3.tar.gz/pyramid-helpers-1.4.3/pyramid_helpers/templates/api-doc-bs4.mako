## -*- coding: utf-8 -*-
<%!
import markdown
%>\
<%
missing_libraries = []
for library in ('moment', 'tempusdominus-bootstrap-4', 'bootstrap-touchspin', 'handlebars'):
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
    % if static_lib_versions.get('tempusdominus-bootstrap-4'):
    <link href="${request.static_path('{0}:static/lib/tempusdominus-bootstrap-4-{1}/build/css/tempusdominus-bootstrap-4.min.css'.format(package, static_lib_versions.get('tempusdominus-bootstrap-4')))}" rel="stylesheet" />
    <script src="${request.static_path('{0}:static/lib/tempusdominus-bootstrap-4-{1}/build/js/tempusdominus-bootstrap-4.min.js'.format(package, static_lib_versions.get('tempusdominus-bootstrap-4')))}"></script>
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
<%def name="parameter_row(service_id, data)">
<%
    id = '{0}-{1}'.format(data['name'].replace('_', '-'), service_id)

    type_label = '{0} of {1}'.format(data['type'], data['items']['type']) if data['type'] in ('ForEach', 'NumberList', 'StringList',) and data['items'] else data['type']
    if data.get('format') is not None:
        type_label = '{0} <mark> {1} </mark>'.format(type_label, data['format'])
    if data.get('min') is not None and data.get('max') is not None:
        type_label = '{0} <mark> {1} <= x <= {2} </mark>'.format(type_label, data['min'], data['max'])
    elif data.get('min') is not None:
        type_label = '{0} <mark> x >= {1} </mark>'.format(type_label, data['min'])
    elif data.get('max') is not None:
        type_label = '{0} <mark> x <= {1} </mark>'.format(type_label, data['max'])

    required_class = 'form-required danger' if data['required'] else ''
    required_prop = 'required' if data['required'] else ''
%>\
\
<tr class="form-group ${required_class}">
    <td><label for="${id}">${data['name']}</label></td>
    <td>
    % if data['type'] in ('Date', 'DateTime'):
        <div id="datetimepicker-${id}" class="input-group input-group-sm date ${data['type'].lower()}picker" data-target-input="nearest">
            <input type="text" class="form-control form-control-sm" id="${id}" name="${data['name']}" data-date-format="${data['format']}" ${required_prop} />
            <div class="input-group-append" data-target="#datetimepicker-${id}" data-toggle="datetimepicker">
                <span class="input-group-text"><i class="fa fa-calendar"></i></span>
            </div>
        </div>
    % elif data['type'] == 'Int':
        <input type="text" class="form-control form-control-sm touchspin" data-bts-min="${data['min'] or -4294967295}" data-bts-max="${data['max'] or 4294967295}" id="${id}" name="${data['name']}" ${required_prop} />
    % elif data['type'] == 'OneOf':
        <select class="form-control form-control-sm selectpicker" id="${id}" name="${data['name']}" ${required_prop} data-minimum-results-for-search="Infinity">
            <option value=""></option>
        % for value in data['values']:
            <option value="${value}">${value}</option>
        % endfor
        </select>
    % elif data['type'] in ('ForEach', 'NumberList', 'StringList',) and data['items'] and data['items']['type'] == 'OneOf':
        <select class="form-control form-control-sm selectpicker" multiple="multiple" id="${id}" name="${data['name']}" ${required_prop} data-minimum-results-for-search="Infinity">
            <option value=""></option>
        % for value in data['items']['values']:
            <option value="${value}">${value}</option>
        % endfor
        </select>
    % elif data['type'] == 'StringBool':
        <select class="form-control form-control-sm selectpicker" id="${id}" name="${data['name']}" ${required_prop} data-minimum-results-for-search="Infinity">
            <option value=""></option>
            <option value="false">${_('False')}</option>
            <option value="true">${_('True')}</option>
        </select>
    % else:
        <input type="text" class="form-control form-control-sm" id="${id}" name="${data['name']}" ${required_prop} />
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
    <div class="col-md-12 d-flex flex-row justify-content-between mb-3">
        <form class="form-inline">
            <div class="input-group input-group-sm">
                <input class="form-control" type="search" id="input-filter" placeholder="${_('Filter')}" aria-label="${_('Filter')}">
                <div class="input-group-append">
                    <div class="input-group-text">
                        <i class="fas fa-filter"></i>
                    </div>
                </div>
            </div>
        </form>

        <button class="btn btn-primary btn-sm" data-toggle="modal" data-target="#help-modal">
            Help <i class="fa fa-question"></i>
        </button>
    </div>
</div>

% if missing_libraries:
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <h4 class="alert-heading">
        <i class="fa fa-ban"></i> ${_('One or more optional libraries are not available!')}
    </h4>
    <ul class="list-unstyled mb-0">
    % for library in missing_libraries:
        <li>${library}</li>
    % endfor
  </ul>
</div>
% endif

% if orphans:
<div class="alert alert-warning alert-dismissible fade show">
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    <h4 class="alert-heading">
        <i class="fa fa-exclamation-triangle"></i> ${_('Orphan routes detected!')}
    </h4>
    <ul class="list-unstyled mb-0">
    % for service in orphans:
        <li>${' / '.join(service['request_methods'])} ${service['pattern']}</li>
    % endfor
  </ul>
</div>
% endif

% if len(modules):
    % for module_name, module in modules.items():
        <% module_id = 'accordion-module-' + module_name.replace('.', '-') %>
<h5 class="module-title" data-toggle="collapse" data-target="#${module_id}" aria-controls="${module_id}">
    ${module['doc'].split('\n')[0] if module['doc'] is not None else _('??? Undocumented module ???')}
    <i class="fa fa-chevron-down fa-sm float-right"></i>
</h5>

<div class="module-group collapse show" id="${module_id}" aria-multiselectable="true">
        % for service in module['services']:
            <% service_id = service['name'].replace('.', '-') %>
            % if not service['allowed'] or (service['doc'] is None and hide_undocumented):
                <% continue %>
            % endif
    <div class="card">
        <div class="card-header p-0 border-bottom-0">
            <h5 class="card-title service-title" data-toggle="collapse" href="#collapse-${service_id}" aria-expanded="true" aria-controls="collapse-${service_id}">
                ## Methods
            % if service['request_methods']:
                <% method = service['request_methods'][0].lower() %>
                % for request_method in service['request_methods']:
                <span class="badge service-method service-method-${method}">${request_method}</span>
                % endfor
            % else:
                <% method = 'unknown' %>
                <span class="badge service-method service-method-unknown">???</span>
            % endif

                ## Path
                <span class="service-path p-2">
                    ${service['pattern']}
                </span>

            % if service['doc']:
                ## Short description: 1st line of docstring
                <span class="service-description p-2 ml-auto service-description-${method}">
                    ${service['doc'].split('\n')[0]}
                </span>
            % endif
            </h5>
        </div>

        <div id="collapse-${service_id}" class="card-collapse collapse" data-parent="#${module_id}" aria-labelledby="heading-${service_id}">
            <div class="card-body service-card-body-${method}">
            % if service['doc']:
                <div class="alert service-doc-${method}">
                    <label class="mb-0">${service['doc'].split('\n')[0]}</label>
                % if len(service['doc'].split('\n')) > 1:
                    <p class="mb-0">${'<br />'.join(service['doc'].split('\n')[1:]) | n}</p>
                % endif
                </div>
            % endif
                <form action="${service['pattern']}" role="form" data-method="${service['request_methods'][0] if service['request_methods'] else ''}">
            % if service['parameters']:
                    <h5>${_('Parameters')}</h5>
                    <table class="table table-sm table-hover table-borderless">
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
                            ${parameter_row(service_id, parameter)}
                % endfor
                        </tbody>
                    </table>
            % endif
                    <div class="float-right">
                        <button class="btn btn-primary" type="submit">${_('Send request')}</button>
                    </div>
                </form>
            </div><!-- .card-body -->
        </div><!-- .card-collapse -->
    </div><!-- .card -->
        % endfor
</div>
    % endfor
% else:
<div class="alert alert-info" role="alert">${_('No API services found')}</div>
% endif

<!-- Help modal -->
<div class="modal fade" id="help-modal" tabindex="-1" role="dialog" aria-labelledby="help-modal-label">
  <div class="modal-dialog modal-xl modal-dialog-scrollable" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="help-modal-label">${_('Help')}</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
          <ul class="nav nav-tabs" role="tablist">
              <li class="nav-item active"><a href="#request-methods" class="nav-link active" aria-controls="request-methods" aria-selected="false" role="tab" data-toggle="tab">Request Methods</a></li>
              <li class="nav-item"><a href="#response-codes" class="nav-link" aria-controls="response-codes" aria-selected="false" aria-selected="false" role="tab" data-toggle="tab">Response Status Codes</a></li>
              <li class="nav-item"><a href="#examples" class="nav-link" aria-controls="examples" aria-selected="false" role="tab" data-toggle="tab">Examples</a></li>
              <li class="nav-item"><a href="#faq" class="nav-link" aria-controls="faq" aria-selected="false" role="tab" data-toggle="tab">FAQ</a></li>
          </ul>

          <div class="tab-content">
              <!-- Request Methods -->
              <div role="tabpanel" class="tab-pane active" id="request-methods">
                  <table class="table">
                      <tbody>
                          <tr>
                              <td align="right"><span class="badge service-method-get">GET</span></td>
                              <td>
                                  <p>The <strong>GET</strong> method is used to **read** (or retrieve) a specific resource (by an identifier) or a collection of resources.</p>

                                  <p>In the “happy” (or non-error) path, <strong>GET</strong> returns a representation in JSON or CSV and an HTTP response code of <mark>200</mark> (OK). In an error case, it most often returns a <mark>404</mark> (NOT FOUND) or <mark>400</mark> (BAD REQUEST).</p>

                                  <p><strong>GET</strong> requests are used only to read data and not change it. Therefore, when used this way, they are considered safe. That is, they can be called without risk of data modification or corruption—calling it once has the same effect as calling it 10 times, or none at all. Additionally, <strong>GET</strong> is idempotent, which means that making multiple identical requests ends up having the same result as a single request.</p>

                                  <p>Parameters must be encoded as a query string (param1=value1&amp;param2=value2&amp;param3=value3...) and append to URL path after a '?'.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="badge service-method-post">POST</span></td>
                              <td>
                                  <p>The <strong>POST</strong> method is most-often utilized to **create** new resources.</p>

                                  <p>On successful creation, return HTTP status <mark>201</mark>, returning a Location header with a link to the newly-created resource.</p>

                                  <p><strong>POST</strong> is neither safe nor idempotent. It is therefore recommended for non-idempotent resource requests. Making two identical <strong>POST</strong> requests will most-likely result in two resources containing the same information.</p>

                                  <p>Parameters must be passed in request body.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="badge service-method-put">PUT</span></td>
                              <td>
                                  <p>The <strong>PUT</strong> method is used to **update** a specific resource (by an identifier) or a collection of resources.</p>

                                  <p>On successful update, return HTTP status <mark>200</mark> (OK).</p>

                                  <p><strong>PUT</strong> is not a safe operation, in that it modifies state on the server, but it is idempotent. In other words, if you update a resource using <strong>PUT</strong> and then make that same call again, the resource is still there and still has the same state as it did with the first call.</p>

                                  <p>Parameters must be passed in request body.</p>
                              </td>
                          </tr>
                          <tr>
                              <td align="right"><span class="badge service-method-delete">DELETE</span></td>
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
                  <dl class="row">
                      <dt class="col-lg-4 text-lg-right">paging</dt>
                      <dd class="col-lg-8">True value enables paging.</dd>
                      <dt class="col-lg-4 text-lg-right">page_size</dt>
                      <dd class="col-lg-8">Allows you to define the number of items that will be returned in each page.</dd>
                      <dt class="col-lg-4 text-lg-right">page</dt>
                      <dd class="col-lg-8">Allows you to define the numero of the desired page.</dd>
                      <dd class="col-lg-8 offset-lg-4"><em>If it's greater than number of pages, no data will be returned.</em></dd>
                  </dl>

                  <h4>Paging information in response</h4>
                  <dl class="row">
                      <dt class="col-lg-4 text-lg-right">pageSize</dt>
                      <dd class="col-lg-8">Number of items requested by page</dd>
                      <dt class="col-lg-4 text-lg-right">page</dt>
                      <dd class="col-lg-8">Numero of the current page</dd>
                      <dt class="col-lg-4 text-lg-right">pageItemCount</dt>
                      <dd class="col-lg-8">Number of items in current page (equal or inferior to pageSize)</dd>
                      <dt class="col-lg-4 text-lg-right">totalItemCount</dt>
                      <dd class="col-lg-8">Total number of items (all pages combined)</dd>
                      <dt class="col-lg-4 text-lg-right">pageStartIndex</dt>
                      <dd class="col-lg-8">Index of the first item</dd>
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
<div class="modal fade" id="response-modal" tabindex="-1" role="dialog" aria-labelledby="response-modal-label" aria-hidden="true">
  <div class="modal-dialog modal-xl modal-dialog-scrollable" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="response-modal-label">${_('Response')}</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
          <h4>${_('Request URL')}</h4>
          <div class="card" id="response-request-url">
              <div class="card-body p-0"><pre class="mb-0"></pre></div>
          </div>

          <div id="response-request-data">
              <h4>${_('Request Data')}</h4>
              <div class="card">
                  <div class="card-body p-0"><pre class="mb-0"></pre></div>
              </div>
          </div>

          <h4>${_('CURL Command')}</h4>
          <div class="card" id="response-request-curl-cmd">
              <div class="card-body p-0"><pre class="mb-0"></pre></div>
          </div>

          <h4>${_('Response Status Code')}</h4>
          <div id="response-code">
              <pre></pre>
          </div>

          <h4>${_('Response Body')}</h4>
          <div class="card" id="response-body">
              <div class="card-body p-0"><pre class="mb-0"></pre></div>
          </div>

          <h4>${_('Response Headers')}</h4>
          <div class="card" id="response-headers">
              <div class="card-body p-0"><pre class="mb-0"></pre></div>
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
