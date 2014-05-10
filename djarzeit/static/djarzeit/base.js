$(document).ready(function () {
    'use strict';
    $('.modal').on('shown', function () {
        $(this).find('.modal-body :input:visible').first().focus();
    });
});
