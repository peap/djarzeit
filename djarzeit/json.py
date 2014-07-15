from copy import deepcopy
from datetime import datetime
import pytz

from django.utils.timezone import now

from timers.models import Timer

SERVER_TIME_FORMAT = '%B %d, %Y, %I:%M %p'

JSON_TEMPLATE_TO_CLIENT = {
    'data': {},
    'error': False,
    'error_msg': '',
    'server_time': None,
    'active_timers': [],
}


def get_server_time(user):
    tz = pytz.timezone(user.profile.timezone)
    return tz.normalize(now())


def get_server_time_str(user):
    return get_server_time(user).strftime(SERVER_TIME_FORMAT)


def get_active_timers(user):
    timers = Timer.objects.filter(category__user=user, active=True)
    return [t.ajax_dict for t in timers]


def get_base_json_data(user):
    response = deepcopy(JSON_TEMPLATE_TO_CLIENT)
    response['server_time'] = get_server_time_str(user)
    response['active_timers'] = get_active_timers(user)
    return response
