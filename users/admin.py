from django.contrib import admin
from . models import User, Student, Teacher
from django.utils.html import format_html

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    actions = ["mark_pending", "mark_approved"] 
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
        
    @admin.action(description="Mark selected student as approved")
    def mark_approved(self, request, queryset):
        queryset.update(status="Approved")
        
        




# admin.site.register(User)
admin.site.register(Student, StudentAdmin)
# admin.site.register(Teacher)