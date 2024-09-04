from django.urls import path
from . import views

urlpatterns = [
    path("exams-event/", views.examList, name="exam-list"),
    path("exams-summary/<str:pk>/", views.examSummary, name="exams-summary"),
    
    
    path("assessment-data/", views.studentResultData, name="assessment-data"),
    path("save-assessment-data/", views.save_assessment_data, name="save_assessment_data"),


]
