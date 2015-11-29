import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now

from categories.models import Category
from categories.views import CategoryDetailView
from core.context import ArZeitContext
from core.json import get_base_json_data
from core.views import ArZeitBaseDetailView, ArZeitTemplateView
from timers.models import Timer


class TimersContext(ArZeitContext):
    active_tab = 'timers'
    auto_refresh = 300
    extra_css = ('timers/timers.css',)
    extra_js = ('timers/timers.js',)


class TimelineContext(ArZeitContext):
    active_tab = 'timeline'
    auto_refresh = 300
    extra_css = ('timers/timeline.css',)
    extra_js = ('core/d3-3.5.9.min.js', 'timers/timeline.js',)


class TimerDetailView(ArZeitBaseDetailView):
    pk_url_kwarg = 'timer_id'

    def get_queryset(self):
        return self.timers

    def process(self):
        pass

    def get_ajax_data(self):
        return {}

    def get_ajax_response(self):
        data = get_base_json_data(self.user)
        data.update(self.get_ajax_data())
        return HttpResponse(json.dumps(data), content_type='application/json')

    def add_error(self, action, msg):
        messages.error(
            self.request,
            'Error {0} timer "{1}": {2}'.format(
                action, self.timer.linkify(), msg),
        )

    def post(self, request, *args, **kwargs):
        self.timer = self.get_object()
        self.process()
        if self.request.is_ajax():
            return self.get_ajax_response()
        else:
            return redirect('timers')


class Listing(ArZeitTemplateView):
    context_class = TimersContext
    template_name = 'timers/timers.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'root_categories': self.root_categories,
            'all_categories': self.sorted_categories,
        })
        return ctx


class New(CategoryDetailView):
    def post(self, request, *args, **kwargs):
        category = self.get_object()
        name = request.POST.get('timer_name')
        action = request.POST.get('create-action')
        timer = Timer(category=category, name=name)
        try:
            timer.full_clean()
        except ValidationError as e:
            msg = 'Error creating new timer: \n'
            for field, errors in e.message_dict.items():
                msg += '{0}: {1}\n'.format(field, ', '.join(errors))
            messages.error(request, msg)
        else:
            timer.save()
            msg = 'Created new timer, {0}'.format(timer.linkify())
            if action == 'create':
                msg += '.'
            if action == 'start':
                timer.start()
                msg += ', and started it.'
            if action == 'archive':
                timer.archive()
                msg += ', and archived it.'
            messages.success(request, msg)
        return redirect('timers')


class Edit(TimerDetailView):
    def process(self):
        name = self.request.POST.get('new_timer_name').strip()
        if not name:
            self.add_error('editing', 'Invalid timer name.')
            return redirect('timers')
        category_id = self.request.POST.get('new_timer_category').strip()
        reportable = bool(self.request.POST.get('new_timer_reportable'))
        try:
            category = self.categories.get(pk=int(category_id))
        except Category.DoesNotExist as e:
            self.add_error('editing', 'Unknown category.')
        except ValueError as e:
            self.add_error('editing', 'Invalid category.')
        else:
            self.timer.name = name
            self.timer.category = category
            self.timer.reportable = reportable
            try:
                self.timer.full_clean()
            except ValidationError as e:
                msg = '\n'
                for field, errors in e.message_dict.items():
                    msg += '{0}: {1}\n'.format(field, ', '.join(errors))
                self.add_error('editing', msg)
            else:
                self.timer.save()
                messages.success(
                    self.request,
                    'Edited timer "{0}".'.format(self.timer.linkify()),
                )


class StartStop(TimerDetailView):
    def process(self):
        if self.timer.active:
            self.timer.stop()
        else:
            self.timer.start()


class Archive(TimerDetailView):
    def process(self):
        if self.timer.archived:
            self.timer.unarchive()
        else:
            self.timer.archive()


class Delete(TimerDetailView):
    def process(self):
        timer = str(self.timer)
        self.timer.delete()
        messages.success(self.request, 'Deleted timer "{0}".'.format(timer))


class Timeline(ArZeitTemplateView):
    context_class = TimelineContext
    template_name = 'timers/timeline.html'
