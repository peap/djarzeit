from django.contrib import messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext
from timers.models import Timer


class TimersContext(ArZeitContext):
    active_tab = 'timers'


@login_required
def timers(request):
    root_categories = Category.objects.filter(user=request.user.id, parent=None)
    active_timers = Timer.objects.filter(
        category__user=request.user.id, active=True)
    context = TimersContext(request, {
        'root_categories': root_categories,
        'active_timers': active_timers,
    })
    return render_to_response('timers/timers.html', {}, context)


@login_required
def new_timer(request):
    name = request.POST.get('timer_name')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(Category, id=category_id)

    timer = Timer(category=category, name=name)
    try:
        timer.full_clean()
    except ValidationError as e:
        msg = 'Error creating new timer - '
        for field, errors in e.message_dict.items():
            msg += '{0}: {1}\n'.format(field, ' '.join(errors))
        messages.error(request, msg)
    else:
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
