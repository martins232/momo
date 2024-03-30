from django.contrib import admin
from django.urls import path, include
from main import settings
from django.conf.urls.static import static

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("admin/password_reset/",auth_views.PasswordResetView.as_view(),name="admin_password_reset",),
    # path("admin/password_reset/done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    # path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm",),
    # path("reset/done/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),
    
    path("", include("users.urls")),
    path("teacher/", include("teachers.urls")),
    path("student/", include("students.urls")),
    path("tinymce/", include('tinymce.urls'),),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "Skodaji Admin"  
admin.site.site_title  =  "Skidaji manager site site"
admin.site.index_title  =  "Skodaji Admin"

handler404 = 'users.views.pageNotFound'