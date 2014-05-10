from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext


class ReportsContext(ArZeitContext):
    active_tab = 'reports'


@login_required
def reports(request):
    context = ReportsContext(request, {})
    return render_to_response('reports/reports.html', {}, context)
