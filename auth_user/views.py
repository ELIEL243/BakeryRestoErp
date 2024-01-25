from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.


def Logout(request):
    logout(request)
    return redirect('home-bakery')


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
            if user.userhasrole.role.name == 'grand stock et boulangerie':
                return redirect('home-bakery')
            elif user.userhasrole.role.name == 'petit stock restaurant':
                return redirect('home-resto')
            elif user.userhasrole.role.name == 'caisse restaurant':
                return redirect('home-facturation')
            elif user.userhasrole.role.name == 'livraison de pack':
                return redirect('home-foodpack')
        else:
            messages.error(request, "echec conn")
            return redirect('login')

    return render(request, 'auth_user/login.html', context={})