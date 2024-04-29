from django.contrib import admin
from . models import User, Student, Teacher, Grade
from . forms import StudentRequestForm
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.core.mail import send_mail


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    actions = ["mark_pending", "mark_approved", "mark_rejected", "remove_rejected"] 
    list_filter = ["status", "grade"]
    list_display = ('name',"grade", 'birth', 'gender', 'image', "action", "_") #Tables you will see
    fields =['birth',"grade", 'gender', 'image', "status"] # forms that could be filled in the admin
    
    
    
    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def _(self, obj): #_ was used so that you can get values for None
        if obj.status == "Approved":
            return True
        elif obj.status == "Pending":
            return None
        else:
            return False
    _.boolean = True
    
    #function to color the text
    def action(self, obj):
        if obj.status == "Approved":
            color = "#28a745"
        elif obj.status == "Pending":
            color = "#fea95e"
        else:
            color = "red"
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.status))
    action.allow_tags = True
    
    
    @admin.action(description="Mark selected student as pending")
    def mark_pending(self, request, queryset):
        queryset.update(status="Pending")
        self.message_user(request, "Student(s) made pending", level=messages.SUCCESS)
        
        
    @admin.action(description="Mark selected student as approved")
    def mark_approved(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Student(s) approved", level=messages.SUCCESS)
        
    @admin.action(description="Mark selected student as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Student(s) rejected", level=messages.SUCCESS)
        
    @admin.action(description="Remove rejected students")
    def remove_rejected(self, request, queryset):
    # Loop over the queryset
        for obj in queryset:
            if obj.status != "Rejected":
                self.message_user(request, "Make sure selected Student has status as rejected", level=messages.INFO)
                break
            else:
                obj.user.delete()
                # Check if the id is not None
                if obj.id is not None:
                    # Delete the object and store the result
                    delete = obj.delete()
                    self.message_user(request,ngettext("%d Student role was succesfully declined. Student deleted",
                                   "%d Student role were successfully declined. Objects deleted", delete) % delete[0], level=messages.SUCCESS)
        
        


class TeacherAdmin(admin.ModelAdmin):
    actions = ["mark_pending", "mark_approved", "mark_rejected", "remove_rejected"] 
    list_filter = ["status"]
    list_display = ( 'name', "phone", 'gender', 'image', "action", "_",) #Tables you will see
    list_display_links = None
    # list_editable = ["status"]
    fields =["phone", 'gender', 'image', "status", ] # forms that could be filled in the admin
    search_fields = ["first_name", "last_name","email", "status"]
    
    
    def save_model(self, request, obj, form, change):
        if obj.status == "Approved":
            obj.user.is_staff = True
            obj.user.save()
        else:
            obj.user.is_staff = False
            obj.user.save()
        super().save_model(request, obj, form, change)

    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def _(self, obj): #_ was used so that you can get values for None
        if obj.status == "Approved":
            return True
        elif obj.status == "Pending":
            return None
        else:
            return False
    _.boolean = True
    
    #function to color the text
    @admin.display(description="STATUS")
    def action(self, obj):
        if obj.status == "Approved":
            color = "#28a745"
        elif obj.status == "Pending":
            color = "#fea95e"
        else:
            color = "red"
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.status))
    action.allow_tags = True
    
    
    @admin.action(description="Mark selected teacher as pending")
    def mark_pending(self, request, queryset):
        queryset.update(status="Pending")
        self.message_user(request, "Teacher(s) made pending", level=messages.SUCCESS)
        
    @admin.action(description="Mark selected teacher as approved")
    def mark_approved(self, request, queryset):
        emails = []
        pending_teachers = queryset.filter(status="Pending")
        for obj in pending_teachers:
            emails.append(obj.user.email)
            # make the admin area accessible to the teachers
            obj.user.is_staff= True
            obj.user.save()
        pending_teachers.update(status="Approved")
        if len(emails)>0:
            send_mail(
                "Approved",
                "Here is the message.",
                emails,
                fail_silently=False,
            ) 
        
       
        self.message_user(request, "Teacher(s) approved", level=messages.SUCCESS)
        
        
    @admin.action(description="Mark selected teacher as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status="Rejected")
        for obj in queryset:
            # make the admin area not accessible to the teachers
            obj.user.is_staff= False
            obj.user.save()
        self.message_user(request, "Teacher(s) rejected", level=messages.SUCCESS)
    @admin.action(description="Remove rejected teachers")
    def remove_rejected(self, request, queryset):
    # Loop over the queryset
        for obj in queryset:
            if obj.status != "Rejected":
                self.message_user(request, "Make sure selected teacher has status as rejected", level=messages.INFO)
                break
            else:
                obj.user.is_teacher=False
                obj.user.is_student = True
                obj.user.save()
                # Check if the id is not None
                if obj.id is not None:
                    # Delete the object and store the result
                    delete = obj.delete()
                    self.message_user(request,ngettext("%d teacher role was succesfully declined. Teacher deleted",
                                   "%d teacher role were successfully declined. Objects deleted", delete) % delete[0], level=messages.SUCCESS)
@admin.register(User)
class MyUserAdmin(DjangoUserAdmin):
    list_display = ["name","username", "role", "email"]
    list_filter = ("is_teacher",)
    fieldsets = (
        (None, {'fields': [("first_name", "last_name"),'username', 'email', 'password']}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important dates", {"fields":("date_joined", "last_login")})
    )
    
    
    def role(self, obj):
        if obj.is_student != None:
            return "Student"
        else:
            return "Teacher"
    
    def name(self, obj):
        return obj.get_full_name()

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Grade)