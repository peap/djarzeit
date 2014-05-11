$(document).ready(function () {

    $('#toggle_all').on('click', function (e) {
        var $button = $(this);
        var old_text = $button.text();
        if (old_text.indexOf('Show') === -1){
            $('.accordion-body').collapse('hide');
            new_text = old_text.replace('Hide', 'Show');
        } else {
            $('.accordion-body').collapse('show');
            new_text = old_text.replace('Show', 'Hide');
        }
        $button.text(new_text);
    });

    $('.panel-body').collapse();
    $('.panel-heading').on('click', function (e) {
        var $panel = $(this).closest('.panel');
        var $panel_body = $panel.find('.panel-body');
        $panel_body.collapse('toggle');
    });

});
