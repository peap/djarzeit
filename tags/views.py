from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import now

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response, TIME_FORMAT
from tags.models import Tags


def tags(request):
    return HttpResponse('hi')


def new_tag(request):
    return HttpResponse('hi')


def tag(request, id):
    tag = get_object_or_404(Tag, id=id, user=request.user)
    context = {
        'tag': tag,
    }
    return HttpResponse('hi')


def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    return redirect('tags')


