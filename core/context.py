from django.template import RequestContext
from django.utils.timezone import now

from core.json import get_server_time_str
from timers.models import Timer


class ArZeitContext(RequestContext):
    active_tab = None
    auto_refresh = 0

    extra_css = ()
    extra_js = ()

    def __init__(self, request, context, **kwargs):
        if request.user.is_authenticated():
            active_timers = Timer.objects.filter(
                category__user=request.user,
                active=True
            )
            server_time = get_server_time_str(request.user)
        else:
            active_timers = []
            server_time = now()
        extra_css = list(self.extra_css) + list(kwargs.pop('extra_css', ()))
        extra_js = list(self.extra_js) + list(kwargs.pop('extra_js', ()))

        context.update({
            'active_tab': self.active_tab,
            'auto_refresh': self.auto_refresh,
            'server_time': server_time,
            'active_timers': active_timers,
            'path': request.path,
            'extra_css': extra_css,
            'extra_js': extra_js,
        })
        super().__init__(request, context, **kwargs)
