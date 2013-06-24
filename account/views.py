from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext


class AccountContext(ArZeitContext):
    app = 'account'


def login(request):
    if request.POST:
        next_url = request.POST.get('next_url')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('timers')
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid login credentials')
        return redirect('home')
    else:
        next_url = request.GET.get('next')
        context = AccountContext(request, {'next_url': next_url})
        return render_to_response('account/login.html', {}, context)


def new_account(request):
    if request.POST:
        name_first = request.POST.get('name_first')
        name_last = request.POST.get('name_last')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user(email, email, password)
            user.first_name = name_first
            user.last_name = name_last
        except IntegrityError as e:
            messages.error(request, e)
            return redirect('home')
        try:
            user.full_clean()
        except ValidationError as e:
            for err in e.message_dict:
                messages.error(request, err)
        else:
            user.save()
            messages.success(request, 'New user created! Please log in.')
        return redirect('home')
    else:
        context = AccountContext(request, {})
        return render_to_response('account/new.html', {}, context)


@login_required
def logout(request):
    dj_logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')


@login_required
def account(request):
    return HttpResponse('hi')
