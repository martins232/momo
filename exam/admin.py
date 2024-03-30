from django.contrib import admin
from . models import Exam, Question, Session
from users.models import User
from django.utils.html import format_html
# Register your models here.
class ExamAdmin(admin.ModelAdmin):
    list_display = ["name", "subject","teacher"]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "teacher":
    #         kwargs["queryset"] = User.objects.filter(is_teacher=True, pk=request.user.pk)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
# class QuestionAdmin(admin.ModelAdmin):
#     # readonly_fields = ["question"]
#     pass




class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score',"action", 'time_started', "time_ended")
    list_display_links = None
    
    @admin.display(description="STATUS")
    def action(self, obj):
        if obj.passed == "Passed":
            color = "#28a745"
        else:
            color = "red"
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.passed))
    action.allow_tags = True
    
admin.site.register(Session, SessionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question)
