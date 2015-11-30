from functools import reduce
import operator
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
            report_date = now().astimezone(tz=user_tz)
    else:
        report_date = now().astimezone(tz=user_tz)
    return user_tz.normalize(report_date.replace(tzinfo=user_tz))


def date_is_today(date):
    tz = date.tzinfo
    nowtz = now().astimezone(tz=tz)
    year, month, day = date.year, date.month, date.day
    return all([year == nowtz.year, month == nowtz.month, day == nowtz.day])


def get_dates_for_week_of(date):
    """
    Get a list of seven datetime objects representing the full week (Monday to
    Sunday) of the given date.
    """
    year, week, dow = date.isocalendar()
    deltas = [(d + 1 - dow) for d in range(7)]
    return [(date + timedelta(days=d)) for d in deltas]


def get_flat_list_of_categories_and_timers(base_cat):
    def _add_to_list(category):
        l = [category]
        l += [t for t in category.timer_set.all()]
        for subcat in category.category_set.all():
            l += _add_to_list(subcat)
        return l
    return _add_to_list(base_cat)


def get_totals_for_dates(base_cat, dates, full=False):
    """
    Get a flat list of 3-tuples for every reportable category and timer of the
    given base category, summarizing the time logged on the given dates. If
    full is True, do this for EVERY category and timer.
    Return format:
    [
        (<category|timer>, total, [time on dates[0], time2 on dates[1], ...]),
        (<category|timer>, total, [time on dates[0], time2 on dates[1], ...]),
    ]
    """
    all_totals = []
    for item in get_flat_list_of_categories_and_timers(base_cat):
        if not full and not item.show_in_selective_reports:
            continue
        totals = [item.get_total_time_on_date(date) for date in dates]
        total = reduce(operator.add, totals)
        if total.total_seconds() > 0:
            all_totals.append((item, total, totals))
    return all_totals
