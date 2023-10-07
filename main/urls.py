from django.contrib import admin
from django.urls import path, include
from main import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("users.urls")),
    path("teacher/", include("teachers.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "Skodaji Admin"  
admin.site.site_title  =  "Skidaji manager site site"
admin.site.index_title  =  "Skodaji Admin"