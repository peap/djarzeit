import re
from datetime import timedelta

from django import template

register = template.Library()

TIMEDELTA_REGEX = re.compile(r'^(.*)(\.[0-9]*)$')


@register.filter
def format_timedelta(value):
    new_value = ''
    if isinstance(value, timedelta):
        hours, remainder = divmod(value.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        new_value = '{0:02}:{1:02}'.format(hours, minutes)
    return new_value


@register.filter
def format_timedelta_long(value):
    new_value = ''
    if isinstance(value, timedelta):
        hours, remainder = divmod(value.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        new_value = '{0:02}:{1:02}:{2:02}'.format(hours, minutes, seconds)
    return new_value


@register.filter
def time_on_date(cat_or_timer, date):
    return cat_or_timer.get_total_time_on_date(date)


@register.filter
def time_on_date_week(cat_or_timer, date):
    return cat_or_timer.get_total_time_on_date_week(date)
