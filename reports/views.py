from django.shortcuts import render_to_response
from django.utils.timezone import datetime, timedelta, now
from django.contrib.auth.decorators import login_required

from categories.models import Category
from core.context import ArZeitContext
from timers.models import Interval
from reports import utils


class ReportsContext(ArZeitContext):
    active_tab = 'reports'
    extra_css = ('reports/reports.css',)


@login_required
def daily_summary(request, full=False):
    report_date = utils.get_report_date(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)

    dates = [report_date]
    totals_by_root_cat = [
        (cat, utils.get_totals_for_dates(cat, dates, full=full))
        for cat in root_categories
        if full or cat.show_in_selective_reports
    ]

    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'dates': dates,
        'totals_by_root_cat': totals_by_root_cat,
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def weekly_summary(request, full=False):
    report_date = utils.get_report_date(request)
    root_categories = Category.objects.filter(user=request.user, parent=None)

    dates = utils.get_dates_for_week_of(report_date)
    totals_by_root_cat = [
        (cat, utils.get_totals_for_dates(cat, dates, full=full))
        for cat in root_categories
        if full or cat.show_in_selective_reports
    ]

    context = ReportsContext(request, {
        'report_date': report_date,
        'root_categories': root_categories,
        'dates': dates,
        'totals_by_root_cat': totals_by_root_cat,
    })
    return render_to_response('reports/summary_base.html', {}, context)


@login_required
def intervals(request):
    report_date = utils.get_report_date(request)
    year, month, day = report_date.year, report_date.month, report_date.day
    tz = report_date.tzinfo
    nowtz = now().astimezone(tz=tz)
    is_today = utils.date_is_today(report_date)

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


@login_required
def totals(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = utils.get_normalized_date(start_date_str, request.user)
    end_date = utils.get_normalized_date(end_date_str, request.user)
    root_categories = Category.objects.filter(user=request.user, parent=None)
    flat_totals_by_root = []
    for cat in root_categories:
        cat_totals = []
        for item in utils.get_flat_list_of_categories_and_timers(cat):
            cat_totals.append(
                (item, item.get_total_time_between_dates(start_date, end_date))
            )
        flat_totals_by_root.append((cat, cat_totals))
    print(flat_totals_by_root)
    context = ReportsContext(request, {
        'start_date': start_date,
        'end_date': end_date,
        'flat_totals_by_root': flat_totals_by_root,
    })
    return render_to_response('reports/totals_between_dates.html', {}, context)


def _get_category_width(num):
    cols_available = 10
    if num > 0:
        width = cols_available // num
        width = width if width > 0 else 1
    else:
        width = cols_available
    return width
