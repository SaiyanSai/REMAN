from django.contrib import admin
from .models import Staff, Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ram_id')


admin.site.register(Staff)
admin.site.register(Student, StudentAdmin)