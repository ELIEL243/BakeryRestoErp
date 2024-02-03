from auth_user.views import get_user_roles


def roles_context(request):
    user = request.user
    if user.is_authenticated:
        roles = get_user_roles(user)
        return {'roles': roles.count()}
    return {'roles': 1}