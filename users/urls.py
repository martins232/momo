from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
# from users.forms import CustomPasswordResetForm

urlpatterns = [
    path("home", views.home, name ="home"),
    path("", views.loginPage, name ="login"),
    path("logout/", views.logoutUser, name ="logout"),
    path("register/", views.register, name ="register"),
    path("lobby/", views.lobby, name ="lobby"),
    path("access-denied/", views.accessDenied, name ="access-denied"),
    path("404/", views.pageNotFound, name ="404"),
    
    path("reset-password", auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path("reset-password-done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset-password-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
]