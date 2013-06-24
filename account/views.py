from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from djarzeit.context import ArZeitContext


class AccountContext(ArZeitContext):
    app = 'account'


def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
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


@login_required
def logout(request):
    return redirect('home')


def account(request):
    '''
    Process account settings changes from modal on base page.
    '''
    return HttpResponse('hi')


def new_account(request):
    '''
    Process new account creation from modal on base page.
    '''
    return HttpResponse('hi')
