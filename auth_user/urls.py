from django.urls import path
from .views import LoginView

urlpatterns = [
    path('', LoginView, name="login"),
    path('logout', LoginView, name="logout"),
    path('admin/logoute/', LoginView, name="logout-admin"),
]