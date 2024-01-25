from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.userhasrole.role.name in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif request.user.userhasrole.role.name not in allowed_roles:
                return HttpResponse("Permission non accordée !")
            return wrapper_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
