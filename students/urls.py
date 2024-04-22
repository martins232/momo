from django.urls import path
from . import views

urlpatterns = [
    path("student-profile/", views.profile, name="student-profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-student-profile"),
    path("image/<str:pk>/", views.editStudentProfileImage, name="edit-student-profile-image"),
    path("available-exams", views.exams, name="available-exam"),
    path("session/", views.session, name="exam-session"),
    path("session/<str:pk>/data", views.session_data, name="exam-data"),
    path("session/<str:pk>/save", views.session_save, name="exam-save"),
    path("completed-session/", views.examResult, name="completed-session"),
    path("session-analysis/<str:pk>/", views.examAnalysis, name="session-analysis"),
    path("session-correction-data/<str:pk>/", views.sessionCorrectionData, name="session-correction-data"), #correction data for students
]
