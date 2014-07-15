from math import ceil
import pytz

from django.contrib import messages
from django.shortcuts import render_to_response
from django.utils.timezone import datetime, timedelta, now
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext
from timers.models import Interval
from reports.utils import get_report_date, date_is_today


class ReportsContext(ArZeitContext):
    active_tab = 'reports'
    extra_css = ('reports/reports.css',)


@login_required
def daily_summary(request):
    report_date = get_report_date(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)

    # TODO
    dates = [report_date]
    all_categories = []

    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'dates': dates,
        'all_categories': all_categories,
        'listing_template': 'reports/daily_summary_listing.html',
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def weekly_summary(request):
    report_date = get_report_date(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)

    # TODO
    dates = [report_date - timedelta(days=1), report_date]
    all_categories = []

    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'dates': dates,
        'all_categories': all_categories,
        'listing_template': 'reports/weekly_summary_listing.html',
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def weekly_by_day(request):
    report_date = get_report_date(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)


@login_required
def intervals(request):
    report_date = get_report_date(request)
    year, month, day = report_date.year, report_date.month, report_date.day
    tz = report_date.tzinfo
    nowtz = now().astimezone(tz=tz)
    is_today = date_is_today(report_date)

    root_categories = Category.objects.filter(user=request.user, parent=None)
    category_width = _get_category_width(root_categories.count())
    user_intervals = Interval.user_intervals(request.user)

    PX_PER_HOUR = 100
    TIME_FORMAT = '%I:%M %p'

    def timedelta_height(td):
        hours = td.total_seconds() / 3600
        height = PX_PER_HOUR * hours
        return int(height)

    min_datetime = datetime(year, month, day, 0, 0, 0, 0, tz)
    max_datetime = datetime(year, month, day, 23, 59, 59, 0, tz)
    all_intervals = user_intervals.filter(
        start__range=(min_datetime, max_datetime),
    ).order_by('start')

    if all_intervals.count() > 0:
        min_interval_time = all_intervals[0].start.astimezone(tz=tz)
        max_interval_time = all_intervals.latest('start').start.astimezone(tz=tz)
        if max_interval_time < nowtz:
            max_interval_time = nowtz
    else:
        min_interval_time = datetime(year, month, day, 8, 0, 0, 0, tz)
        max_interval_time = datetime(year, month, day, 18, 0, 0, 0, tz)

    def time_top(dt):
        temp_min_time = min_interval_time.replace(minute=0, second=0)
        offset = dt - temp_min_time
        return timedelta_height(offset)

    time_cells = []
    for hour in range(min_interval_time.hour, max_interval_time.hour+1):
        start_time = datetime(year, month, day, hour, 0, 0, 0, tz)
        an_hour = timedelta(hours=1)
        time_cells.append({
            'height': timedelta_height(an_hour),
            'top': time_top(start_time),
            'value': start_time.strftime(TIME_FORMAT),
            'classes': 'time-cell',
        })
    if is_today:
        time_cells.append({
            'height': 1,
            'top': time_top(nowtz),
            'value': '',
            'classes': 'current-time',
        })

    root_category_cells = []
    for cat in root_categories:
        interval_list = []
        for interval in all_intervals:
            if interval.timer.category.root_parent == cat:
                interval_list.append(interval)
        cells = []
        for interval in interval_list:
            start = interval.start.astimezone(tz=tz).strftime(TIME_FORMAT)
            end = '[active]'
            if interval.end is not None:
                end = interval.end.astimezone(tz=tz).strftime(TIME_FORMAT)
            title = '{0} ({1}-{2})'.format(
                interval.timer.hierarchy_display, start, end)
            cells.append({
                'height': timedelta_height(interval.length),
                'top': time_top(interval.start.astimezone(tz=tz)),
                'interval': interval,
                'timer': interval.timer,
                'title': title,
                'start': start,
                'end': end,
            })
        root_category_cells.append((cat, cells))

    context = {
        'report_date': report_date,
        'category_width': category_width,
        'total_height': timedelta_height(max_interval_time - min_interval_time),
        'time_cells': time_cells,
        'root_category_cells': root_category_cells,
    }
    context = ReportsContext(
        request,
        context,
    )
    return render_to_response('reports/intervals.html', {}, context)


def _get_category_width(num):
    cols_available = 10
    if num > 0:
        width = cols_available // num
        width = width if width > 0 else 1
    else:
        width = cols_available
    return width
