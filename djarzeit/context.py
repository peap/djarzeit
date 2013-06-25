from django.template import RequestContext
from django.utils.timezone import now

from timers.models import Timer


class ArZeitContext(RequestContext):
    tab = None

    def __init__(self, request, context, **kwargs):
        active_timers = Timer.objects.filter(
            category__user=request.user.id,
            active=True
        )
        context.update({
            'tab': self.tab,
            'server_time': now(),
            'active_timers': active_timers,
            'path': request.path,
        })
        super().__init__(request, context, **kwargs)
