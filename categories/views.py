from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext
from categories.models import Category


class CategoriesContext(ArZeitContext):
    app = 'categories'


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user.id)
    context = CategoriesContext(request, {
        'categories': categories,
    })
    return render_to_response('categories/categories.html', {}, context)


@login_required
def new_category(request):
    parent_id = request.POST.get('category_parent_id')
    if parent_id == 'root':
        parent_cat = None
    else:
        try:
            parent_cat = Category.objects.get(pk=int(parent_id))
        except (ValueError, ObjectDoesNotExist) as e:
            messages.error(request, 'Please choose a valid parent category.')
            return redirect('categories')
    name = request.POST.get('category_name')
    if not name:
        messages.error(request, 'Please choose a category name.')
        return redirect('categories')

    category = Category()
    category.user = request.user
    category.parent = parent_cat
    category.name = request.POST.get('category_name')
    category.description = request.POST.get('category_desc')
    category.full_clean()
    category.save()
    messages.success(request, 'Created a new category.')

    return redirect('categories')


@login_required
def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        'category': category,
    }
    return render_to_response('timers/category.html', context)


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('categories')
