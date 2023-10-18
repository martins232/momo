from django.urls import path
from . import views

urlpatterns = [
    path("student-profile/", views.profile, name="student-profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-student-profile"),
    path("image/<str:pk>/", views.editStudentProfileImage, name="edit-student-profile-image"),
]
