from django.template import RequestContext
from django.utils.timezone import now

from timers.models import Timer

class ArZeitContext(RequestContext):
    active_tab = None
    auto_refresh = 0

    extra_css = ()
    extra_js = ()

    def __init__(self, request, context, **kwargs):
        active_timers = Timer.objects.filter(
            category__user=request.user.id,
            active=True
        )
        extra_css = list(self.extra_css) + list(kwargs.pop('extra_css', ()))
        extra_js = list(self.extra_js) + list(kwargs.pop('extra_js', ()))

        context.update({
            'active_tab': self.active_tab,
            'auto_refresh': self.auto_refresh,
            'server_time': now(),
            'active_timers': active_timers,
            'path': request.path,
            'extra_css': extra_css,
            'extra_js': extra_js,
        })
        super().__init__(request, context, **kwargs)
