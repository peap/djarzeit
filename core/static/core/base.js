$(document).ready(function () {
    'use strict';
    $('.modal').on('shown.bs.modal', function (e) {
        $(this).find('.modal-body :input:visible:first').focus();
    });
});
