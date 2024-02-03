from django.http import HttpResponse
from .views import get_user_roles


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            roles = get_user_roles(request.user)
            check = False
            for i in roles:
                if i.role.name in allowed_roles:
                    check = True
            if check:
                print("Permission accordé")
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Permission non accordée !")
            #return wrapper_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
