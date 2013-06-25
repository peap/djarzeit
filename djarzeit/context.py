from django.template import RequestContext
from django.utils.timezone import now


class ArZeitContext(RequestContext):
    app = None

    def __init__(self, request, context, **kwargs):
        context.update({
            'app': self.app,
            'server_time': now(),
        })
        super().__init__(request, context, **kwargs)
