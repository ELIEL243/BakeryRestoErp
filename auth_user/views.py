from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.


def Logout(request):
    logout(request)
    return redirect('login')


def LogoutAdmin(request):
    logout(request)
    return redirect('admin/')


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username
                            , password=password)

        if user is not None:
            login(request, user)
            user = User.objects.get(username=username)
            if user.userhasrole.role.name == 'bakery':
                return redirect('home-bakery')

        else:
            messages.error(request, "echec conn")
            return redirect('login')

    return render(request, 'auth_user/login.html', context={})