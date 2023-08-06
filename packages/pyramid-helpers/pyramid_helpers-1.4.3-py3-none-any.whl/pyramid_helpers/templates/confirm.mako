## -*- coding: utf-8 -*-
<%inherit file="/site.mako" />
<%def name="head()">
${parent.head()}
    <script type="text/javascript">
$(document).ready(function() {
    $('#confirm-dialog').modal().on('hidden.bs.modal', function(event) {
        // Perform cancel action when the dialog is closed by user
        $(this).find('button[name="cancel"]').click();
    });
});
    </script>
</%def>\
<section>
    <div id="confirm-dialog" class="modal" role="dialog">
        <div class="modal-dialog">
            <div class="modal-content">
                <form method="post" role="form">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">${_('Confirmation')}</h4>
                    </div>
                    <div class="modal-body">
                        <strong>${question}</strong>
% if note:
                        <br><br>
                        <em>${note | n}</em>
% endif
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-default" name="confirm">${_('Ok')}</button>
                        <button type="submit" class="btn btn-primary" name="cancel">${_('Cancel')}</button>
                    </div>
                </form>
            </div><!-- End of modal-content -->
        </div><!-- End of modal-dialog -->
    </div><!-- End of modal -->
</section>
