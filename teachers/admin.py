from django.contrib import admin
from . models import Subject
from django.utils.html import format_html


# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "assign_teacher")
    list_filter   = ["assigned", "teacher"]
    
    ordering = ["assigned"]
    
    
    @admin.display(description="Status")
    def assign_teacher(self, obj):

        if obj.teacher != None and obj.assigned==True:
            obj.code = "Assigned"
            color = "#28a745"
        else:
            obj.code ="Not assigned"
            color = "red"
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.code ))
    assign_teacher.allow_tags=True
    
admin.site.register(Subject, SubjectAdmin)
