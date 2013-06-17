from django.shortcuts import render_to_response


def home(request):
    context = {}
    return render_to_response('timers/timers.html', context)
