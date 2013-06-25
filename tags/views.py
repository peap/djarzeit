from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext
from tags.models import Tag


class TagsContext(ArZeitContext):
    app = 'tags'


@login_required
def tags(request):
    tags = Tag.objects.filter(user=request.user.id)
    context = TagsContext(request, {
        'tags': tags,
    })
    return render_to_response('tags/tags.html', {}, context)


@login_required
def new_tag(request):
    return HttpResponse('hi')


@login_required
def tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    context = {
        'tag': tag,
    }
    return HttpResponse('hi')


@login_required
def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    tag.delete()
    return redirect('tags')


