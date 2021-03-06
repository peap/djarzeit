$(document).ready(function () {

    $('form.startstop-form').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        var data = $form.serialize();
        var url = $form.attr('action');
        $.post(url, data, function(data){
            updatePageData(data);
            var $form_btns = $form.find('button');
            var $startstop_btn = $form.find('button[type="submit"]');
            var old_text = $startstop_btn.text().trim();
            if (old_text === 'Start') {
                $form.closest('.root-category-panel')
                     .find('form.startstop-form button')
                     .removeClass('btn-danger').addClass('btn-success');
                $form.closest('.root-category-panel')
                     .find('form.startstop-form button[type="submit"]')
                     .text('Start');
                $form_btns.removeClass('btn-success').addClass('btn-danger');
                $startstop_btn.text('Stop');
            } else {
                $form_btns.removeClass('btn-danger').addClass('btn-success');
                $startstop_btn.text('Start');
            }
        });
    });

    $('a.create-timer-and-more').on('click', function (e) {
        var $this = $(this);
        $this.next('button[type="submit"]').click();
    });

});

function updatePageData(data){
    $('#server_time').text(data.server_time);
    var $active = $('#active-timers');
    if (data.active_timers.length === 0) {
        $active.text('Active: (none)');
    } else {
        var timers = [];
        for (var i = 0; i < data.active_timers.length; i++) {
            var timer = data.active_timers[i];
            timers.push(
                '<a href="#timer_' + timer.id + '" ' +
                'title="' + timer.hierarchy + '">' +
                timer.name + '</a>'
            );
        }
        $active.html('Active: ' + timers.join(', '));
    }
    document.title = document.title.replace(
        /[0-9]+ active/,
        data.active_timers.length + ' active'
    );
}
