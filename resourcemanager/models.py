from django.db import models

# Create your models here.
class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, null = False)

class Student(models.Model):
    user = user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ram_id = models.CharField(max_length=20, null = False)
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
