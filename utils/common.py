from django.contrib.auth import login, logout

def process_login(request, user):
    login(request, user)
    request.session['uid'] = user.id

def process_logout(request):
    logout(request)
