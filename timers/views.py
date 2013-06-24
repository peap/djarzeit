from datetime import datetime
from json import dumps

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import now

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response, TIME_FORMAT
from timers.models import Category, Timer, Interval, Tags


def timers(request):
    categories = Category.objects.all()
    active_timers = Timer.objects.filter(active=True)
    context = {
        'categories': categories,
        'active_timers': active_timers,
        'server_time': now().strftime(TIME_FORMAT)
    }
    context = ArZeitContext(request, context)
    return render_to_response('timers/home.html', {}, context)


def new_timer(request):
    category_id = request.POST.get('category_id')
    name = request.POST.get('timer_name')
    if not category_id:
        messages.error(request, 'Please choose a category for this new timer.')
        return redirect('home')
    if not name:
        messages.error(request, 'Please choose a timer name.')
        return redirect('home')

    category = get_object_or_404(Category, id=category_id)
    timer = Timer()
    timer.category = category
    timer.name = name
    timer.full_clean()
    timer.save()
    messages.success(request, 'Created a new timer.')

    return redirect('home')


def delete_timer(request, id):
    timer = get_object_or_404(Timer, id=id)
    timer.delete()
    return redirect('home')


def timer(request, id):
    timer = get_object_or_404(Timer, id=id)
    context = {
        'timer': timer,
    }
    return render_to_response('timers/timer.html', context)


def startstop(request, id):
    timer = get_object_or_404(Timer, id=id)

    if timer.active:
        timer.stop()
    else:
        timer.start()

    return redirect('home')
