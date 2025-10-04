# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # кастомна реєстрація
    path("register/", views.register_view, name="register"),

    # стандартні login/logout (але з кастомними шаблонами)
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    # профіль
    # path("profile/", views.profile_view, name="profile"),
    path("", views.profile_view, name="profile"),  # доступно на /profile/
]
