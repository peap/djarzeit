from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext


class AccountContext(ArZeitContext):
    app = 'account'


def login(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid login credentials')
        return redirect('home')
    else:
        context = AccountContext(request, {})
        return render_to_response('account/login.html', {}, context)


def new_account(request):
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
    else:
        context = AccountContext(request, {})
        return render_to_response('account/new.html', {}, context)


@login_required
def logout(request):
    logout(request, request.user)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')


@login_required
def account(request):
    return HttpResponse('hi')
