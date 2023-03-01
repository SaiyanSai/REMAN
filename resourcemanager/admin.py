from django.contrib import admin
from .models import Staff, Student, Device, Allowed_Users, Device_logs #, Uniquekeys

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ram_id')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'hall', 'room_number')

#admin.site.register(Uniquekeys)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Staff)
admin.site.register(Student, StudentAdmin)
admin.site.register(Allowed_Users)
admin.site.register(Device_logs)