from django.urls import path
from .views import LoginView, Logout, modules_space

urlpatterns = [
    path('', LoginView, name="login"),
    path('modules_space/', modules_space, name="module-spaces"),
    path('logout', Logout, name="logout"),
    path('admin/logoute/', LoginView, name="logout-admin"),
]