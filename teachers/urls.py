from django. urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-profile"),
    path("image/<str:pk>/", views.editProfileImage, name="edit-profile-image"),
    path("exam/", views.createExam, name="exam"),
    path("exam/<str:pk>/edit/", views.editExam, name="edit-exam"),
    path("exam/<str:pk>/delete/", views.deleteExam, name="delete-exam"),
    path("exam/<str:pk>/", views.viewExam, name="view-exam"),
    path("exam/questions", views.viewAllQuestions, name="all-questions"),
    path("exam/<str:pk>/question/edit/", views.editQuestion, name="view-question"),
    path("exam/<str:pk>/question/delete/", views.deleteQuestion, name="delete-question"),
]
