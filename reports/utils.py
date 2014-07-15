import pytz

from django.contrib import messages
from django.utils.timezone import datetime, timedelta, now


def get_report_date(request):
    user_tz = pytz.timezone(request.user.profile.timezone)
    date_string = request.GET.get('report_date')
    if date_string:
        try:
            report_date = datetime.strptime(date_string, '%m/%d/%Y')
        except ValueError:
            messages.error(request, 'Invalid date.')
            report_date = datetime.today()
    else:
        report_date = datetime.today()
    return user_tz.normalize(report_date.replace(tzinfo=user_tz))


def date_is_today(date):
    tz = date.tzinfo
    nowtz = now().astimezone(tz=tz)
    year, month, day = date.year, date.month, date.day
    return all([year == nowtz.year, month == nowtz.month, day == nowtz.day])


def get_dates_for_week_of(date):
    year, week, dow = date.isocalendar()
    deltas = [(d + 1 - dow) for d in range(7)]
    return [(date + timedelta(days=d)) for d in deltas]
