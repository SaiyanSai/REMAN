from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    # path('givedata/',views.givedata, name = 'givedata'),   example http end point
]