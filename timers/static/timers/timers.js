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
        var $clicked_col = $(e.target).closest('div');
        if ($clicked_col.attr('data-toggle') === 'add_timer') {
            var $target = $($clicked_col.attr('data-target'));
            if ($target.is(':visible')) {
                $target.addClass('hide');
            } else {
                $target.removeClass('hide');
            }
        } else {
            $panel_body.collapse('toggle');
        }
    });

});
