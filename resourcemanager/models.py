from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, date

# Create your models here.
#class Uniquekeys(models.Model):
#    unikey = models.CharField(max_length=20, null=False)

class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, null = False)

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ram_id = models.CharField(max_length=20, null = False)
    rfid_uid = models.CharField(max_length =8, default= "00000000")
    EET = 'EET'
    CET = 'CET'
    MET = 'MET'
    cource_choices = [(EET, 'EET'),(CET, 'CET'),(MET, 'MET')]
    course = models.CharField(
        null = False,
        max_length= 5,
        choices= cource_choices,
        default = EET
    )

class Allowed_Users(models.Model):
    user = models.ForeignKey(Student, on_delete = models.CASCADE)

class Device(models.Model):
    device_id = models.CharField(max_length=10, null=False)
    device_manufacturer = models.CharField(max_length=20, null=False)
    device_name = models.CharField(max_length=20, null=False)
    room_number = models.IntegerField()
    allowed_users = models.ManyToManyField(Allowed_Users)
    lupton = 'Lupton'
    gleeson = 'Gleeson'
    whitmann = 'Whitmann'
    hall_choices = [(lupton, 'Lupton'),(gleeson, 'Gleeson'),(whitmann, 'Whitmann')]
    hall = models.CharField(null = False,
                            max_length = 10,
                            choices = hall_choices,
                            default = lupton)
    


class Device_logs(models.Model): #Scan Date is missing add that
    user = models.ForeignKey(Student, on_delete = models.CASCADE)
    username = models.CharField(max_length=20, null=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    dev_id = models.CharField(max_length=20, null=False)
    ram_id = models.CharField(max_length = 20, null = False)
    room_number = models.IntegerField()
    hall = models.CharField(max_length=10, null = False)
    timeoflogin = models.TimeField(default = datetime.now())
    dateoflogin = models.DateField(date.today(), default=date.today())

class ActiveDevices(models.Model):
    d_id = models.CharField(max_length = 20, null = False )
    d_name = models.CharField(max_length = 20, null = False)
    d_hall = models.CharField(max_length = 10, null = False)
    d_room = models.IntegerField()