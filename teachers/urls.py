from django. urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit-profile/<str:pk>/", views.editProfile, name="edit-profile"),
    path("image/<str:pk>/", views.editProfileImage, name="edit-profile-image"),
    path("exam/", views.scheduledExam, name="scheduled-exam"),
    path("closed-exam/", views.closedExam, name="closed-exam"),
    path("exam/<str:pk>/edit/", views.editExam, name="edit-exam"),
    path("exam/delete/", views.deleteExam, name="delete-exam"),
    # path("exam/<str:pk>/", views.viewExam, name="view-exam"),
    # path("exam/<str:pk>/question/edit/", views.editQuestion, name="view-question"),
    path("exam/<str:pk>/question/delete/", views.deleteQuestion, name="delete-question"),
    path("session-dashboard/<str:pk>/", views.sessionDashboard, name="session-dashboard"),
    path("analysis/<str:pk>/", views.studentPerformance, name="student-performance"),
    path("exam-dashboard/<str:pk>/", views.examDashboard, name="exam-dashboard"),
    path("new-exam-dashboard/<str:pk>/", views.newExamDashboard, name="new-exam-dashboard"),
    
    
    path("all-topics/", views.allTopics, name="all-topics"),
    path("add-topic/", views.addTopic, name="add-topic"),
    path("topic-data/", views.topicsData, name="topic-data"),
    path("edit-topic/", views.editTopic, name="edit-topic"),
    path("delete-topic/", views.deleteTopic, name="delete-topic"),
    
    
    path("questions", views.allQuestions, name="all-questions"),
    path("question-data", views.questionData, name="question-data"),
    
    # path("create-question", views.createQuestion, name="create-question"),
    # path("delete-question", views.deleteQuestion, name="delete-question"),
    # path("edit-question", views.editQuestion, name="edit-question"),
    
    
    #debugging-------------------------------------------
    path("create-myquestion", views.question_create, name="create-myquestion"),
    path("edit-myquestion/<str:pk>/", views.question_edit, name="edit-myquestion"),
    path("delete-myquestion/", views.question_delete, name="delete-myquestion"),
    #debugging-------------------------------------------
    
    
    path("session-data/<str:pk>/", views.sessionDashboardData, name="session-data"),
    path("exam-data/<str:pk>/", views.examDashboardData, name="exam-data"),
   
    
    
    path("exam/<str:pk>/", views.viewExam, name="view-exam"),
    path("assign-question-to-exam/<str:pk>/", views.assignQuestionToExam, name="assign-question-to-exam"),
    path("remove-question-from-exam/<str:pk>/", views.removeQuestionFromExam, name="remove-question-from-exam"),
]
