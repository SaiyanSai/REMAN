from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('studentregister/', views.student_register, name='studentregister'),
    path('login/', views.login_request, name='login'),
    path('sconfpage/',views.sconfpage,name='sconfpage'),
    path('logout/', views.logout_request, name='logout'),
    path('deviceregister/',views.device_register, name='device_register'),
    path('staffregister/', views.staff_register, name = 'staffregister'),
    path('givedata/',views.givedata, name = 'givedata'),  # example http end point
    path('devicelogs/', views.devicelogs, name = 'devicelogs'),
]