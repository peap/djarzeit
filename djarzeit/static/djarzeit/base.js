$(document).ready(function () {
    'use strict';
    $('.modal').on('show.bs.modal', function (e) {
        $(this).find('.modal-body :input:visible').first().focus();
    });
});
