from datetime import datetime

from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from categories.models import Category
from djarzeit.context import ArZeitContext


def parse_date_or_today(date_string):
    if date_string:
        try:
            report_date = datetime.strptime(date_string, '%m/%d/%Y')
        except ValueError:
            report_date = datetime.today()
    else:
        report_date = datetime.today()
    return report_date


class ReportsContext(ArZeitContext):
    active_tab = 'reports'


@login_required
def reports(request):
    context = ReportsContext(request, {})
    return render_to_response('reports/reports.html', {}, context)


@login_required
def daily_summary(request):
    report_date = parse_date_or_today(request.GET.get('report_date'))
    context = ReportsContext(request, {
        'report_date': report_date,
        'categories': Category.objects.filter(user=request.user),
    })
    return render_to_response('reports/daily_summary.html', {}, context)


@login_required
def weekly_summary(request):
    context = ReportsContext(request, {})
    return render_to_response('reports/weekly_summary.html', {}, context)


@login_required
def intervals(request):
    context = ReportsContext(request, {})
    return render_to_response('reports/intervals.html', {}, context)
