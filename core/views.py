import pytz

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.generic.detail import BaseDetailView

from core.context import ArZeitContext
from timers.models import Timer


class ArZeitViewMixin:

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.tz = pytz.timezone(self.user.profile.timezone)
        return super().dispatch(request, *args, **kwargs)

    @property
    def categories(self):
        return self.user.category_set.all()

    @property
    def sorted_categories(self):
        return sorted(self.categories, key=lambda c: c.hierarchy_display)

    @property
    def root_categories(self):
        return self.categories.filter(parent=None)

    @property
    def timers(self):
        return Timer.objects.filter(category__user=self.user)

    @property
    def active_timers(self):
        return self.timers.filter(active=True)


class ArZeitView(ArZeitViewMixin, View):
    pass


class ArZeitBaseDetailView(ArZeitViewMixin, BaseDetailView):
    pass


class ArZeitTemplateView(ArZeitViewMixin, TemplateView):
    context_class = ArZeitContext

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'active_timers': self.active_timers,
        })
        return self.context_class(self.request, ctx, **kwargs)
