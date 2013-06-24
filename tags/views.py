from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.utils.timezone import now

from djarzeit.context import ArZeitContext
from djarzeit.json import get_new_json_response, TIME_FORMAT
from tags.models import Tag


class TagsContext(ArZeitContext):
    app = 'tags'


def tags(request):
    tags = Tag.objects.filter(user=request.user)
    context = TagsConext(request, {
        'tags': tags,
    })
    return render_to_response(request, {}, context)


def new_tag(request):
    return HttpResponse('hi')


def tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    context = {
        'tag': tag,
    }
    return HttpResponse('hi')


def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    return redirect('tags')


