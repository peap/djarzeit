from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render_to_response
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from account.models import Profile
from djarzeit.context import ArZeitContext


class AccountContext(ArZeitContext):
    active_tab = 'account'


def login(request):
    if request.user.is_authenticated():
        return redirect('timers')
    if request.POST:
        next_url = request.POST.get('next_url')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
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
        name_first = request.POST.get('new_name_first')
        name_last = request.POST.get('new_name_last')
        email = request.POST.get('new_email')
        username = request.POST.get('new_username')
        password = request.POST.get('new_password')
        try:
            user = User.objects.create_user(username, email, password)
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
            profile = Profile(user=user, timezone=settings.TIME_ZONE)
            profile.full_clean()
            profile.save()
            messages.success(request, 'New user created!')
            user = authenticate(username=username, password=password)
            dj_login(request, user)
        return redirect('timers')
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
    next_url = request.POST.get('next_url')
    user = request.user
    user.profile.timezone = request.POST.get('user_timezone')
    try:
        user.profile.full_clean()
    except ValidationError as e:
        for field, errors in e.message_dict.items():
            messages.error(
                request,
                'Error updating profile - {0}: {1}'.format(
                    field, errors,
                )
            )
    else:
        user.profile.save()
        messages.success(request, 'Saved user profile.')
    if next_url:
        return redirect(next_url)
    return redirect('home')
