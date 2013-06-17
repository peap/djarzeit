from django.contrib import messages
from django.shortcuts import render_to_response, redirect, get_object_or_404

from djarzeit.json import get_new_json_response
from timers.models import Timer, Interval, Tags


def home(request):
    timers = Timer.objects.all()
    context = {
        'timers': timers,
    }
    return render_to_response('timers/timers.html', context)


def timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    context = {
        'timer': timer,
    }
    return render_to_response('timers/timer.html', context)


# TODO: create an AJAX-only decorator
def startstop(request, timer_id):
    if not request.is_ajax():
        messages.error('Invalid request.')
        return redirect('home')

    timer = get_object_or_404(Timer, id=timer_id)

    if time.active:
        timer.stop()
    else:
        timer.start()

    response = get_new_json_response()
    return response
