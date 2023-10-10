from django.contrib import admin
from . models import Exam
from users.models import User
# Register your models here.
class ExamAdmin(admin.ModelAdmin):
    pass
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "teacher":
    #         kwargs["queryset"] = User.objects.filter(is_teacher=True, pk=request.user.pk)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Exam, ExamAdmin)
