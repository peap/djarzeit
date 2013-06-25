from django.template import RequestContext
from django.utils.timezone import now
from django.core.context_processors import csrf

from djarzeit.json import TIME_FORMAT


class ArZeitContext(RequestContext):
    app = None

    def __init__(self, request, context, **kwargs):
        context.update({
            'app': self.app,
            'server_time': now(),
        })
        context.update(csrf(request))
        super().__init__(request, context, **kwargs)
