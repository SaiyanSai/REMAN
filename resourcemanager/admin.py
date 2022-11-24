from django.contrib import admin
from .models import Staff, Student, Device

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ram_id')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'hall', 'room_number')

admin.site.register(Device, DeviceAdmin)
admin.site.register(Staff)
admin.site.register(Student, StudentAdmin)