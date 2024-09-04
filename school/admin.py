from django.contrib import admin
from .models import AcademicYear, School, Level,Grade, Term


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'motto', 'contact_numbers', 'created', 'updated')
    search_fields = ('name', 'motto', 'address')
    list_filter = ('created', 'updated')

admin.site.register(School, SchoolAdmin)
admin.site.register(Level)
admin.site.register(Grade)
admin.site.register(AcademicYear)
admin.site.register(Term)
