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
    root_categories = Category.objects.filter(user=request.user, parent=None)
    all_categories = Category.objects.filter(user=request.user)
    all_categories = sorted(all_categories, key=lambda cat: cat.hierarchy_display)
    active_timers = Timer.objects.filter(
        category__user=request.user, active=True)
    context = {
        'root_categories': root_categories,
        'all_categories': all_categories,
        'active_timers': active_timers,
    }
    context = TimersContext(
        request,
        context,
        extra_css=['timers/timers.css'],
        extra_js=['timers/timers.js'],
    )
    return render_to_response('timers/timers.html', {}, context)


@login_required
def startstop(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    if timer.active:
        timer.stop()
    else:
        timer.start()
    return redirect('timers')


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


@login_required
def edit_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    name = request.POST.get('new_timer_name').strip()
    if not name:
        messages.error(request, 'Invalid timer name.')
        return redirect('timers')
    category_id = request.POST.get('new_timer_category').strip()
    try:
        category = Category.objects.get(user=request.user, pk=int(category_id))
    except Category.DoesNotExist as e:
        messages.error(request, 'Unknown category.')
        return redirect('timers')
    except ValueError as e:
        messages.error(request, 'Invalid category.')
        return redirect('timers')
    timer.name = name
    timer.category = category
    timer.full_clean()
    timer.save()
    messages.success(request, 'Successfully edited timer.')
    return redirect('timers')


@login_required
def delete_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    timer.delete()
    messages.success(request, 'Deleted timer.')
    return redirect('timers')
