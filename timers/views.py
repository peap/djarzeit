from datetime import datetime
from json import dumps

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response, TIME_FORMAT
from timers.models import Category, Timer, Interval, Tags


def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'server_time': datetime.now().strftime(TIME_FORMAT)
    }
    context = ArZeitContext(request, context)
    return render_to_response('timers/home.html', {}, context)


def new_category(request):
    name = request.POST.get('category_name')
    if not name:
        messages.error(request, 'Please choose a category name.')
        return redirect('home')

    category = Category()
    category.name = request.POST.get('category_name')
    category.full_clean()
    category.save()
    messages.success(request, 'Created a new category.')

    return redirect('home')


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


def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        'category': category,
    }
    return render_to_response('timers/category.html', context)


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
