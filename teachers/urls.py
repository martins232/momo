from django. urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-profile"),
]
