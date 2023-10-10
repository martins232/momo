from django. urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-profile"),
    path("exam/", views.createExam, name="exam"),
    path("exam/<str:pk>/delete", views.deleteExam, name="delete-exam"),
    path("exam/<str:pk>/edit", views.editExam, name="edit-exam"),
]
