from django.template import RequestContext
from django.utils.timezone import now

from timers.models import Timer

TABS = ('timers', 'categories', 'tags', 'reports')


class ArZeitContext(RequestContext):
    active_tab = None

    def __init__(self, request, context, **kwargs):
        active_timers = Timer.objects.filter(
            category__user=request.user.id,
            active=True
        )
        context.update({
            'TABS': TABS,
            'active_tab': self.active_tab,
            'server_time': now(),
            'active_timers': active_timers,
            'path': request.path,
        })
        super().__init__(request, context, **kwargs)
