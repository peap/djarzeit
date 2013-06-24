from datetime import datetime
from json import dumps

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import now

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response, TIME_FORMAT
from timers.models import Category, Timer, Interval, Tags


def categories(request):
    return HttpResponse('hi')


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


def delete_category(request, id):
    # TODO: Delete child categories
    # TODO: Delete child timers
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('home')


def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        'category': category,
    }
    return render_to_response('timers/category.html', context)
