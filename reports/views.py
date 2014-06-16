import pytz

from django.shortcuts import render_to_response
from django.contrib import messages
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext


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
def reports(request):
    context = ReportsContext(request, {})
    return render_to_response('reports/reports.html', {}, context)


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
    context = ReportsContext(request, {})
    return render_to_response('reports/intervals.html', {}, context)
