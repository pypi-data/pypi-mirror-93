<%!
import pprint
%>\
<%namespace name="form" file="/form-tags.mako"/>\
<%inherit file="/site.mako" />\
<div class="page-header">
    <h2>${_('Validators')}</h2>
</div>
<%form:form name="validators_form" method="post" enctype="multipart/form-data">
    <%form:hidden name="hidden_input" />
    <fieldset>
        <legend>${_('Standard inputs')}</legend>

        <div class="form-group">
            <label for="text-input">${_('Text')}</label>
            <%form:text id="text-input" name="text_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="textarea-input">${_('Text area')}</label>
            <%form:textarea id="textarea-input" name="textarea_input" class_="form-control"></%form:textarea>
        </div>

        <div class="form-group">
            <label for="password-input">${_('Password')}</label>
            <%form:password id="password-input" name="password_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label>
                <%form:checkbox id="checkbox-input" name="checkbox_input" value="true" />
                ${_('Checkbox')}
            </label>
        </div>

        <div class="form-group">
            <label>
                <%form:radio id="radio-input-1" name="radio_input" value="one" />
                ${_('Radio (One)')}
            </label>
            <label>
                <%form:radio id="radio-input-2" name="radio_input" value="two" />
                ${_('Radio (Two)')}
            </label>
            <label>
                <%form:radio id="radio-input-3" name="radio_input" value="three" />
                ${_('Radio (Three)')}
            </label>
            <label>
                <%form:radio id="radio-input-4" name="radio_input" value="invalid" />
                ${_('Radio (Invalid)')}
            </label>
        </div>

        <div class="form-group">
            <label for="select-input1">${_('Select (Numbers)')}</label>
            <%form:select id="select-input1" name="select_input1" class_="form-control">
                <%form:option value="">--</%form:option>
                <%form:option value="one">${_('One')}</%form:option>
                <%form:option value="two">${_('Two')}</%form:option>
                <%form:option value="three">${_('Three')}</%form:option>
                <%form:option value="invalid">${_('Invalid')}</%form:option>
            </%form:select>
        </div>

        <div class="form-group">
            <label for="select-input2">${_('Select (Fruits)')}</label>
            <%form:select id="select-input2" name="select_input2" class_="form-control">
                <%form:option value="">--</%form:option>
                <%form:optgroup label="${_('Fruits')}">
                    <%form:option value="apple">${_('Apple')}</%form:option>
                    <%form:option value="banana">${_('Banana')}</%form:option>
                    <%form:option value="orange">${_('Orange')}</%form:option>
                </%form:optgroup>
                <%form:optgroup label="${_('Numbers')}">
                    <%form:option value="one">${_('One')}</%form:option>
                    <%form:option value="two">${_('Two')}</%form:option>
                    <%form:option value="three">${_('Three')}</%form:option>
                </%form:optgroup>
            </%form:select>
        </div>

        <div class="form-group">
            <label for="upload-input">${_('Upload')}</label>
            <%form:upload id="upload-input" name="upload_input" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${_('Number inputs')}</legend>

        <div class="form-group">
            <label for="number-input">${_('Number')}</label>
            <%form:number id="number-input" name="number_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="range-input">${_('Range')} (0-100)</label>
            <%form:range id="range-input" name="range_input" class_="form-control" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${_('Communication inputs')}</legend>

        <div class="form-group">
            <label for="url-input">${_('Url')}</label>
            <%form:url id="url-input" name="url_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="email-input">${_('Email')}</label>
            <%form:email id="email-input" name="email_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="tel-input">${_('Tel')}</label>
            <%form:tel id="tel-input" name="tel_input" class_="form-control" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" placeholder="000-000-0000" />
        </div>
    </fieldset>

    <fieldset>
        <legend>${_('Date/time inputs')}</legend>

        <div class="form-group">
            <label for="time-input">${_('Time')}</label>
            <%form:time id="time-input" name="time_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="week-input">${_('Week')}</label>
            <%form:week id="week-input" name="week_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="month-input">${_('Month')}</label>
            <%form:month id="month-input" name="month_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="date-input">${_('Date')}</label>
            <%form:date id="date-input" name="date_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="datetime-local-input">${_('Datetime local')}</label>
            <%form:datetime_local id="datetime-local-input" name="datetime_local_input" class_="form-control" placeholder="YYYY-MM-DDTHH:MM"/>
        </div>

        <div class="form-group">
            <label for="datetime-naive-input">${_('Datetime UTC (naive)')}</label>
            <%form:datetime_local id="datetime-naive-input" name="datetime_naive_input" class_="form-control" placeholder="YYYY-MM-DDTHH:MM"/>
        </div>
    </fieldset>

    <fieldset>
        <legend>${_('Miscellaneous inputs')}</legend>

        <div class="form-group">
            <label for="color-input">${_('Color')}</label>
            <%form:color id="color-input" name="color_input" class_="form-control" />
        </div>

        <div class="form-group">
            <label for="list-input">${_('List')}</label>
            <%form:text id="list-input" name="list_input" class_="form-control" />
        </div>
    </fieldset>

    <div class="form-group text-right">
        <input class="btn btn-primary" type="submit" name="submit_input" value="${_('Submit')}" />
    </div>
</%form:form>

% if errors:
<h3>${_('Errors')}</h3>
<pre>${pprint.pformat(errors)}</pre>
% elif result:
<h3>${_('Result')}</h3>
<pre>${pprint.pformat(result)}</pre>
% endif
