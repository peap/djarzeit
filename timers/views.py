from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from categories.models import Category
from categories.views import CategoryDetailView
from djarzeit.context import ArZeitContext
from djarzeit.views import ArZeitBaseDetailView, ArZeitTemplateView
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

    def process(self):
        pass

    def add_error(self, action, msg):
        messages.error(
            self.request,
            'Error {0} timer "{1}": {2}'.format(action, self.timer, msg),
        )

    def add_success(self, action):
        messages.success(
            self.request,
            'Successfully {0} timer "{1}".'.format(action, self.timer),
        )

    def post(self, request, *args, **kwargs):
        self.timer = self.get_object()
        self.process()
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
            messages.success(
                request,
                'Successfully created new timer "{0}".'.format(timer),
            )
        return redirect('timers')


class Edit(TimerDetailView):
    def process(self):
        name = self.request.POST.get('new_timer_name').strip()
        if not name:
            self.add_error('editing', 'Invalid timer name.')
            return redirect('timers')
        category_id = self.request.POST.get('new_timer_category').strip()
        try:
            category = self.categories.get(pk=int(category_id))
        except Category.DoesNotExist as e:
            self.add_error('editing', 'Unknown category.')
        except ValueError as e:
            self.add_error('editing', 'Invalid category.')
        else:
            self.timer.name = name
            self.timer.category = category
            try:
                self.timer.full_clean()
            except ValidationError as e:
                msg = '\n'
                for field, errors in e.message_dict.items():
                    msg += '{0}: {1}\n'.format(field, ', '.join(errors))
                self.add_error('editing', msg)
            else:
                self.timer.save()
                self.add_success('edited')


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
        self.timer.delete()
        self.add_success('deleted')
