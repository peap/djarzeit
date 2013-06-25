import re
from datetime import timedelta

from django import template

register = template.Library()

TIMEDELTA_REGEX = re.compile(r'^(.*)(\.[0-9]*)$')

@register.filter
def format_timedelta(value):
    new_value = ''
    if isinstance(value, timedelta):
        new_value = str(value)
        match = TIMEDELTA_REGEX.match(new_value)
        if match is not None:
            new_value = match.groups()[0]
    return new_value
