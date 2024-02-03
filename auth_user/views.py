from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import AffectedRoles

# Create your views here.


def get_user_roles(utilisateur):
    roles = AffectedRoles.objects.filter(user=utilisateur)
    return roles


def redirect_user_role(request, utilisateur):
    roles = get_user_roles(utilisateur)
    role = None
    for i in roles:
        role = i.role.name
    print(role)
    if role == 'grand stock et boulangerie':
        return redirect('home-bakery')
    elif role == 'petit stock restaurant':
        print("je marche !")
        return redirect('home-resto')
    elif role == 'caisse restaurant':
        return redirect('home-facturation')
    elif role == 'livraison de pack':
        return redirect('home-foodpack')
    return HttpResponse("")


def Logout(request):
    logout(request)
    return redirect('home-bakery')


def LogoutAdmin(request):
    logout(request)
    return redirect('admin/')


def LoginView(request):
    role = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username
                            , password=password)

        if user is not None:
            login(request, user)
            #user = User.objects.get(username=username)
            roles = get_user_roles(user)
            if roles.count() > 1:
                return redirect('module-spaces')
            elif roles.count() == 1:
                for i in roles:
                    role = i.role.name
                if role == 'grand stock et boulangerie':
                    return redirect('home-bakery')
                elif role == 'petit stock restaurant':
                    return redirect('home-resto')
                elif role == 'caisse restaurant':
                    return redirect('home-facturation')
                elif role == 'livraison de pack':
                    return redirect('home-foodpack')
        else:
            messages.error(request, "echec conn")
            return redirect('login')

    return render(request, 'auth_user/login.html', context={})


def modules_space(request):
    roles = get_user_roles(request.user)
    return render(request, 'auth_user/select_module.html', context={'roles': roles})
