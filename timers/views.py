from json import dumps

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response
from timers.models import Timer, Interval, Tags


def home(request):
    timers = Timer.objects.all()
    context = {
        'timers': timers,
    }
    context = ArZeitContext(request, context)
    return render_to_response('timers/timers.html', {}, context)


def new(request):
    timer = Timer()
    timer.name = request.POST.get('timer_name')
    timer.full_clean()
    timer.save()
    json = get_new_json_response()
    json['data']['id'] = timer.id
    return HttpResponse(dumps(json))


def timer(request, id):
    timer = get_object_or_404(Timer, id=id)
    context = {
        'timer': timer,
    }
    return render_to_response('timers/timer.html', context)


# TODO: create an AJAX-only decorator
def startstop(request, id):
    if not request.is_ajax():
        messages.error('Invalid request.')
        return redirect('home')

    timer = get_object_or_404(Timer, id=id)

    if time.active:
        timer.stop()
    else:
        timer.start()

    json = get_new_json_response()
    return HttpResponse(dumps(json))
