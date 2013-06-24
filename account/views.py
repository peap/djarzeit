from django.http import HttpResponse


def account(request):
    '''
    Process account settings changes from modal on base page.
    '''
    return HttpResponse('hi')


def login(request):
    '''
    Process a login request.
    '''
    return HttpResponse('hi')


def new_account(request):
    '''
    Process new account creation from modal on base page.
    '''
    return HttpResponse('hi')
