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
                $target.find('input[name=timer_name]').focus();
            }
        } else {
            $panel_body.collapse('toggle');
        }
    });

    $('form.startstop-form').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        var data = $form.serialize();
        var url = $form.attr('action');
        $.post(url, data, function(data){
            var $form_btns = $form.find('button');
            var $startstop_btn = $form.find('button[type="submit"]');
            var old_text = $startstop_btn.text().trim();
            if (old_text === 'Start') {
                $form.closest('.root-category-panel').find('button')
                     .removeClass('btn-danger').addClass('btn-success');
                $form.closest('.root-category-panel').find('button[type="submit"]')
                     .text('Start');
                $form_btns.removeClass('btn-success').addClass('btn-danger');
                $startstop_btn.text('Stop');
            } else {
                $form_btns.removeClass('btn-danger').addClass('btn-success');
                $startstop_btn.text('Start');
            }
        });
    });

});

