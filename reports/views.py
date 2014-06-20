from math import ceil
import pytz

from django.contrib import messages
from django.shortcuts import render_to_response
from django.utils.timezone import datetime, timedelta
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext
from timers.models import Interval


def parse_date_or_today(request):
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


class ReportsContext(ArZeitContext):
    active_tab = 'reports'


@login_required
def daily_summary(request):
    report_date = parse_date_or_today(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)
    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'listing_template': 'reports/daily_summary_listing.html',
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def weekly_summary(request):
    report_date = parse_date_or_today(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)
    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'listing_template': 'reports/weekly_summary_listing.html',
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def intervals(request):
    report_date = parse_date_or_today(request)
    year, month, day = report_date.year, report_date.month, report_date.day
    tz = report_date.tzinfo
    root_categories = Category.objects.filter(user=request.user, parent=None)
    user_intervals = Interval.user_intervals(request.user)
    min_datetime = datetime(year, month, day, 6, 0, 0, 0, tz)
    max_datetime = datetime(year, month, day, 20, 59, 59, 0, tz)

    root_category_intervals = []
    for cat in root_categories:
        interval_list = user_intervals.filter(
            timer__category=cat,
            start__range=(min_datetime, max_datetime),
        ).order_by('start')
        root_category_intervals.append((cat, interval_list))

    rows = []
    for hour in range(6, 21):
        hour_min = datetime(year, month, day, hour, 0, 0, 0, tz)
        hour_max = datetime(year, month, day, hour, 59, 59, 0, tz)
        cells = [{'rowspan': 1, 'value': hour_min.strftime('%H:%M')}]
        for cat, intervals in root_category_intervals:
            rowspan = 1
            value = ''
            previous_timer_active = False
            for interval in intervals:
                if interval.active_at(hour_min):
                    previous_timer_active = True
                if interval.start >= hour_min and interval.start < hour_max:
                    rowspan = ceil((
                        interval.length.total_seconds() /
                        (hour_max-hour_min).total_seconds()
                    ) / (60 * 60))
                    if value:
                        value += ' / ' + str(interval.timer)
                    else:
                        value += str(interval.timer)
            if not previous_timer_active or value:
                cells.append({'rowspan': rowspan, 'value': value})
        rows.append(cells)

    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'rows': rows,
    })
    return render_to_response('reports/intervals.html', {}, context)
