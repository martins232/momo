from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name ="home"),
    path("login/", views.loginPage, name ="login"),
    path("logout/", views.logoutUser, name ="logout"),
    path("register/", views.register, name ="register"),
    path("lobby/", views.lobby, name ="lobby"),
    path("access-denied/", views.accessDenied, name ="access-denied"),
    path("404/", views.pageNotFound, name ="404"),
]