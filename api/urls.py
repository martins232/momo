from django.urls import path
from . import views

urlpatterns = [
    path("exams-event/", views.examList, name="exam-list"),
    path("exams-summary/<str:pk>/", views.examSummary, name="exams-summary"),
]
