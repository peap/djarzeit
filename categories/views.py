from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
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
    name = request.POST.get('category_name')
    if not name:
        messages.error(request, 'Please choose a category name.')
        return redirect('categories')

    category = Category()
    category.user = request.user
    category.name = request.POST.get('category_name')
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
