from django.contrib import admin
from . models import User, Student, Teacher
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib import messages

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    actions = ["mark_pending", "mark_approved", "mark_rejected"] 
    list_filter = ["status"]
    list_display = ('name', 'birth', 'gender', 'image', "action", "_") #Tables you will see
    fields =['birth', 'gender', 'image', "status"] # forms that could be filled in the admin
    
    
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
        
        


class TeacherAdmin(admin.ModelAdmin):
    actions = ["mark_pending", "mark_approved", "mark_rejected", "remove_rejected"] 
    list_filter = ["status"]
    list_display = ('name', 'email',"phone", 'gender', 'image', "action", "_") #Tables you will see
    fields =['email',"phone", 'gender', 'image', "status", ] # forms that could be filled in the admin
    search_fields = ["first_name", "last_name","email", "status"]
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
    
    
    @admin.action(description="Mark selected student as pending")
    def mark_pending(self, request, queryset):
        queryset.update(status="Pending")
        self.message_user(request, "Teacher(s) made pending", level=messages.SUCCESS)
        
    @admin.action(description="Mark selected student as approved")
    def mark_approved(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Teacher(s) approved", level=messages.SUCCESS)
        
    @admin.action(description="Mark selected student as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Teacher(s) rejected", level=messages.SUCCESS)
    @admin.action(description="Remove rejected teachers")
    def remove_rejected(self, request, queryset):
    # Loop over the queryset
        for obj in queryset:
            if obj.status != "Rejected":
                self.message_user(request, "Make sure selected Teacher has status as rejected", level=messages.INFO)
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

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(User)