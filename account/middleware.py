import pytz

from django.utils import timezone


class TimeZoneActivationMiddleware():
    def process_request(self, request):
        if request.user.is_authenticated():
            tzname = request.user.profile.timezone
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
