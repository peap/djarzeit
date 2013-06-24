from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404

from djarzeit.context import ArZeitContext
from categories.models import Category


class CategoriesContext(ArZeitContext):
    app = 'categories'


def categories(request):
    categories = Category.objects.filter(user=request.user)
    context = CategoriesContext(request, {
        'categories': categories,
    })
    return render_to_response('categories/categories.html', {}, context)


def new_category(request):
    name = request.POST.get('category_name')
    if not name:
        messages.error(request, 'Please choose a category name.')
        return redirect('home')

    category = Category()
    category.name = request.POST.get('category_name')
    category.full_clean()
    category.save()
    messages.success(request, 'Created a new category.')

    return redirect('home')


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('home')


def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        'category': category,
    }
    return render_to_response('timers/category.html', context)
