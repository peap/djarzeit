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
        new_value = '{0:02}h {1:02}\' {2:02}"'.format(hours, minutes, seconds)
    return new_value
