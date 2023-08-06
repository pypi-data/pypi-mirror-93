/*
 * pyramid-helpers -- Helpers to develop Pyramid applications
 * By: Cyril Lacoux <clacoux@easter-eggs.com>
 *     Valéry Febvre <vfebvre@easter-eggs.com>
 *
 * Copyright (C) 2011-2021 Cyril Lacoux, Easter-eggs
 * https://gitlab.com/yack/pyramid-helpers
 *
 * This file is part of pyramid-helpers.
 *
 * pyramid-helpers is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * pyramid-helpers is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


var $responseModal;
var templates = {};

var reRoute = /(\{[_a-zA-Z][^{}]*(?:\{[^{}]*\}[^{}]*)*\})/g;
var reRouteOld = /(\:[_a-zA-Z]\w*)/g;

function clearFormErrors($context) {
    $('.input-error', $context).remove();
}

function setFormErrors(errors, $context) {
    clearFormErrors($context);

    $.each(errors, function(field, message) {
        var $input;
        var isMultiple = false;
        var position;
        var values;

        field = field.split('-');
        if (field.length === 2) {
            // Field is multiple. Field data type is NumberList, StringList or ForEach
            isMultiple = true;
            position = parseInt(field.pop(1));
        }
        field = field[0];

        $input = $(':input[name="' + field + '"]', $context);
        if (isMultiple) {
            values = $input.val().split(',');
            message = values[position] + ': ' + message;
        }

        if ($input.length === 1) {
            $input.after(templates.formError({message: message}));
        }
    });
}

function showResponse(url, method, parameters, responseData, responseDataType, jqXHR) {
    var curlCmd;
    var requestUrl = url;

    // Construct curl command
    curlCmd = 'curl';
    if (!parameters.format || parameters.format === 'json') {
        curlCmd += " -H 'Accept:application/json'";
    }
    else if (parameters.format === 'csv') {
        curlCmd += " -H 'Accept:text/csv'";
    }

    curlCmd += ' -X ' + method;

    if (method == 'GET' && !$.isEmptyObject(parameters)) {
        requestUrl += '?' + $.param(parameters);
    }
    else if (!$.isEmptyObject(parameters)) {
        $.each(parameters, function(name, value) {
            curlCmd += " \\\n    -d '" + name + '=' + decodeURIComponent(value) + "'";
        });
    }

    curlCmd += " \\\n    '" + requestUrl + "'";

    // Request URL
    $responseModal.find('#response-request-url pre').text(requestUrl);

    // curl command
    $responseModal.find('#response-request-curl-cmd pre').text(curlCmd);

    // Request Data
    if (method != 'GET' && !$.isEmptyObject(parameters)) {
        $responseModal.find('#response-request-data pre').html(
            JSON.stringify(parameters, undefined, 4)
        );
        $responseModal.find('#response-request-data').show();
    }
    else {
        $responseModal.find('#response-request-data').hide();
    }

    // Response Code
    $responseModal.find('#response-code pre').text(jqXHR.status);
    if (jqXHR.status < 400) {
        $responseModal.find('#response-code pre').removeClass('bg-danger').addClass('bg-success');
    }
    else {
        $responseModal.find('#response-code pre').removeClass('bg-success').addClass('bg-danger');
    }

    // Response Body
    if ($.type(responseData) === 'object') {
        responseData = JSON.stringify(responseData, undefined, 4);
        var $exportLink = $('<a />')
            .html('<i class="fa fa-download"> </i>')
            .css('position', 'absolute')
            .css('right', '24px')
            .attr('download', 'response.json')
            .attr('href', 'data:application/json;charset=utf8,' + encodeURIComponent(responseData));

        $responseModal.find('#response-body pre')
            .html(syntaxHighlight(responseData))
            .prepend($exportLink);
    }
    else {
        $responseModal.find('#response-body pre').text(responseData);
    }

    // Response Headers
    $responseModal.find('#response-headers pre').text(jqXHR.getAllResponseHeaders());

    $responseModal.modal('show');
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            }
            else {
                cls = 'string';
            }
        }
        else if (/true|false/.test(match)) {
            cls = 'boolean';
        }
        else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

/*
 * Global initialization
 */
$(function() {
    $responseModal = $('#response-modal');

    $responseModal.on('hide.bs.modal', function(e) {
        $responseModal.find('.modal-body').scrollTop(0);
    });

    $('.module-group.collapse').on('show.bs.collapse', function(e) {
        $(this).prev().find('i').removeClass('fa-chevron-right').addClass('fa-chevron-down');
    });
    $('.module-group.collapse').on('hide.bs.collapse', function(e) {
        $(this).prev().find('i').removeClass('fa-chevron-down').addClass('fa-chevron-right');
    });
    $('.card-collapse.collapse').on('shown.bs.collapse', function(e) {
        $('html, body').animate({
            scrollTop: $(e.currentTarget).parent().offset().top - ($('nav.main-header').outerHeight() + 4)
        }, 500);
    });

    // Filter
    $('#input-filter').on('keyup change', function(e) {
        var tokens = $(this).val().split(' ')
            .filter(function(token, i, array) {
                return token !== '';
            })
            .map(function(token, i, array) {
                return token.toLowerCase();
            });
        var regex = new RegExp(tokens.join('|'), 'g');

        $.each($('.card'), function(i, card) {
            var $card = $(card);
            var path = $card.find('span.service-path').text().toLowerCase();
            var description = $card.find('span.service-description').text().toLowerCase();

            if (path.match(regex) || description.match(regex)) {
                $card.show();
            }
            else {
                $card.hide();
            }
       });
    }).trigger('change');

    // Pre-compile form error template
    templates.formError = Handlebars.compile($('#form-error').html());

    if ($.fn.TouchSpin) {
        $('.touchspin').TouchSpin({
            buttondown_class: 'btn btn-default',
            buttonup_class: 'btn btn-default'
        });

        // Hack: Bootstrap TouchSpin (at least until v4.2.5) doesn't handle buttons size
        $.each($('.touchspin'), function(i, el) {
            if ($(el).hasClass('form-control-sm')) {
                $(el).parent().addClass('input-group-sm');
            }
        });
    }

    $('form').on('submit', function(e) {
        e.preventDefault();

        var $form = $(this);
        var method = $form.data('method');

        // Add spinner icon in submit button
        $form.find('button[type="submit"]').prepend('<i class="fas fa-circle-notch fa-spin mr-1"></i>');

        if (!method) {
            alertify.notify(_('Invalid API service: missing request method'), 'error');
            return;
        }

        var parameters = {};
        $.each($form.find(':input[name]'), function(i, input) {
            var value = $(input).val();
            if (value.length > 0) {
                parameters[input.name] = $.isArray(value) ? value.join(',') : value;
            }
        });

        var url = this.getAttribute('action');

        // Map URL path pattern with input values
        $.each(url.match(reRoute) || [], function(i, match) {
            // remove '{' and '}' characters (first and last positions)
            var predicate = match.substr(1, match.length - 2);
            // remove expression if exists like in {name:expr} pattern
            predicate = predicate.split(':')[0];
            url = url.replace(match, parameters[predicate]);
            delete parameters[predicate];
        });
        // Map URL with input values (old pattern language)
        $.each(url.match(reRouteOld) || [], function(i, match) {
            // Remove ':' character (first position)
            var predicate = match.substr(1);
            url = url.replace(match, parameters[predicate]);
            delete parameters[predicate];
        });

        var dataType = parameters.format && parameters.format !== 'json' ? 'text' : 'json';

        $.ajax({
            url: url,
            method: method,
            data: parameters,
            dataType: dataType
        })
        .done(function(data, textStatus, jqXHR) {
            clearFormErrors($form);

            showResponse(url, method, parameters, data, dataType, jqXHR);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            if (jqXHR.status >= 500) {
                alertify.notify(_('Failed to communicate with server'), 'error');
                return;
            }

            var data = jqXHR.responseJSON || JSON.parse(jqXHR.responseText);

            if (data) {
                showResponse(url, method, parameters, data, dataType, jqXHR);

                if (data.errors) {
                    setFormErrors(data.errors, $form);
                }
                else {
                    clearFormErrors($form);
                }
            }
        })
        .always(function() {
            // Remove spinner icon in submit button
            $form.find('button[type="submit"]').find('i').remove();
        });
    });
});
