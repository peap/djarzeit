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
    action = 'modified'

    def get_queryset(self):
        return self.timers

    def clean_and_save(self, timer):
        try:
            timer.full_clean()
        except ValidationError as e:
            msg = 'Error - '
            for field, errors in e.message_dict.items():
                msg += '{0}: {1}\n'.format(field, ' '.join(errors))
            messages.error(self.request, msg)
        else:
            timer.save()
            messages.success(
                self.request,
                'Successfully {0} timer: {1}.'.format(self.action, timer)
            )


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


class EditTimer(TimerDetailView):
    action = 'edited'

    def post(self, request, *args, **kwargs):
        timer = self.get_object()
        name = request.POST.get('new_timer_name').strip()
        if not name:
            messages.error(request, 'Invalid timer name.')
            return redirect('timers')
        category_id = request.POST.get('new_timer_category').strip()
        try:
            category = self.categories.get(pk=int(category_id))
        except Category.DoesNotExist as e:
            messages.error(request, 'Unknown category.')
        except ValueError as e:
            messages.error(request, 'Invalid category.')
        else:
            timer.name = name
            timer.category = category
            self.clean_and_save(timer)
        return redirect('timers')


class ArchiveTimer(TimerDetailView):
    def post(self, request, *args, **kwargs):
        timer = self.get_object()
        if timer.archived:
            timer.unarchive()
        else:
            timer.archive()
        return redirect('timers')


@login_required
def delete_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id, category__user=request.user)
    timer.delete()
    messages.success(request, 'Deleted timer: {0}.'.format(timer))
    return redirect('timers')
