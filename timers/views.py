from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from categories.models import Category
from categories.views import CategoryDetailView
from djarzeit.context import ArZeitContext
from djarzeit.views import ArZeitView, ArZeitBaseDetailView, ArZeitTemplateView
from timers.models import Timer


class TimersContext(ArZeitContext):
    active_tab = 'timers'
    auto_refresh = 300
    extra_css = ('timers/timers.css',)
    extra_js = ('timers/timers.js',)


class TimerDetailView(ArZeitBaseDetailView):
    pk_url_kwarg = 'timer_id'

    def get_queryset(self):
        return self.timers


class TimersListing(ArZeitTemplateView):
    context_class = TimersContext
    template_name = 'timers/timers.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'root_categories': self.root_categories,
            'all_categories': self.sorted_categories,
        })
        return ctx


class NewTimer(CategoryDetailView):
    def post(self, request, *args, **kwargs):
        category = self.get_object()
        name = request.POST.get('timer_name')
        category_id = request.POST.get('category_id')
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
            messages.success(request, 'Created new timer: {0}.'.format(timer))
        return redirect('timers')


class StartStop(TimerDetailView):
    def post(self, request, *args, **kwargs):
        timer = self.get_object()
        if timer.active:
            timer.stop()
        else:
            timer.start()
        return redirect('timers')


@login_required
def edit_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, category__user=request.user)
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
    messages.success(request, 'Edited timer: {0}.'.format(timer))
    return redirect('timers')


@login_required
def archive_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, category__user=request.user)
    if timer.archived:
        messages.error(request, 'Timer already archived.')
        return redirect('timers')
    timer.archived = True
    timer.full_clean()
    timer.save()
    messages.success(request, 'Archived timer: {0}.'.format(timer))
    return redirect('timers')


@login_required
def unarchive_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, category__user=request.user)
    if not timer.archived:
        messages.error(request, 'Timer not archived.')
        return redirect('timers')
    timer.archived = False
    timer.full_clean()
    timer.save()
    messages.success(request, 'Un-archived timer: {0}.'.format(timer))
    return redirect('timers')


@login_required
def delete_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, category__user=request.user)
    timer.delete()
    messages.success(request, 'Deleted timer: {0}.'.format(timer))
    return redirect('timers')
