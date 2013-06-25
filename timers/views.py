from datetime import datetime
from json import dumps

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response
from timers.models import Timer, Interval


class TimersContext(ArZeitContext):
    app = 'timers'


@login_required
def timers(request):
    root_categories = Category.objects.filter(user=request.user.id, parent=None)
    active_timers = Timer.objects.filter(category__user=request.user.id, active=True)
    context = TimersContext(request, {
        'root_categories': root_categories,
        'active_timers': active_timers,
    })
    return render_to_response('timers/timers.html', {}, context)


@login_required
def new_timer(request):
    category_id = request.POST.get('category_id')
    name = request.POST.get('timer_name')
    if not category_id:
        messages.error(request, 'Please choose a category for this new timer.')
        return redirect('timers')
    if not name:
        messages.error(request, 'Please choose a timer name.')
        return redirect('timers')

    category = get_object_or_404(Category, id=category_id)
    timer = Timer()
    timer.category = category
    timer.name = name
    timer.full_clean()
    timer.save()
    messages.success(request, 'Created a new timer.')

    return redirect('timers')


def timer(request, id):
    timer = get_object_or_404(Timer, id=id)
    context = {
        'timer': timer,
    }
    return render_to_response('timers/timer.html', context)


@login_required
def startstop(request, id):
    timer = get_object_or_404(Timer, id=id)
    if timer.active:
        timer.stop()
    else:
        timer.start()
    return redirect('timers')


@login_required
def delete_timer(request, id):
    timer = get_object_or_404(Timer, id=id)
    timer.delete()
    messages.success(request, 'Deleted timer.')
    return redirect('timers')
