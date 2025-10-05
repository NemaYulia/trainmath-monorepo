# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # кастомна реєстрація
    path("register/", views.register_view, name="register"),

    # стандартні login/logout (але з кастомними шаблонами)
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),

    # профіль
    path("profile/", views.profile_view, name="profile"),
]
