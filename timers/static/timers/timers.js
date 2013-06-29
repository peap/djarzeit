$.ajaxSetup({
    type: 'POST',
    error: defaultAjaxError,
    statusCode: {
        404: defaultAjax404,
    },
});

$(document).ready(function(){
     $('#toggle_all').on('click', toggleAll);
//    $('.startstop_form').on('submit', function(event){
//        event.preventDefault();
//        startStopTimer($(this));
//    });
});

function toggleAll(){
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
}

function startStopTimer($form){
    var url = $form.attr('action');
    var data = $form.serialize();
    var settings = {
        data: data,
        success: defaultAjaxSuccess,
    }
    $.ajax(url, settings);
}

function defaultAjaxSuccess(response, textStatus, jqXHR){
    var server_time = response.data.server_time;
    $('#server_time').text(server_time);
}

function defaultAjaxError(jqXHR, textStatus, errorThrown){
    $('#messages ul').append('<li>'+textStatus+'</li>');
} 

function defaultAjax404(jqXHR, textStatus, errorThrown){
    alert('Received 404; could not find requested item.');
} 
