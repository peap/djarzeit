from django.contrib import messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token

from djarzeit.context import ArZeitContext
from djarzeit.views import ArZeitBaseDetailView
from categories.models import Category

FAKE_ROOT_PARENT = {
    'id': 'root',
    'name': 'Root',
    'description': 'The root "category" to which all categories belong',
}


class CategoriesContext(ArZeitContext):
    active_tab = 'categories'


class CategoryDetailView(ArZeitBaseDetailView):
    pk_url_kwarg = 'category_id'

    def get_queryset(self):
        return self.categories


@login_required
@requires_csrf_token
def categories(request):
    root_categories = Category.objects.filter(user=request.user, parent=None)
    context = {
        'root_categories': root_categories,
        'FAKE_ROOT_PARENT': FAKE_ROOT_PARENT,
    }
    context = CategoriesContext(
        request,
        context,
        extra_css=['categories/categories.css'],
        extra_js=['categories/categories.js'],
    )
    return render_to_response('categories/categories.html', {}, context)


@login_required
def new_category(request, cat_id):
    if cat_id == 'root':
        parent_cat = None
    else:
        try:
            parent_cat = Category.objects.get(pk=int(cat_id))
        except (ValueError, ObjectDoesNotExist) as e:
            messages.error(request, 'Please choose a valid parent category.')
            return redirect('categories')
    name = request.POST.get('category_name')
    if not name:
        messages.error(request, 'Please choose a category name.')
        return redirect('categories')
    category = Category(
        user=request.user,
        parent=parent_cat,
        name=request.POST.get('category_name'),
        description=request.POST.get('category_desc'),
    )
    category.full_clean()
    category.save()
    messages.success(request, 'Created new category.')
    return redirect('categories')


@login_required
def category(request, cat_id):
    category = get_object_or_404(Category, pk=int(cat_id))
    context = {
        'category': category,
    }
    return render_to_response('category/category.html', context)


@login_required
def delete_category(request, cat_id):
    category = get_object_or_404(Category, pk=int(cat_id))
    category.delete()
    messages.success(request, 'Deleted category.')
    return redirect('categories')
