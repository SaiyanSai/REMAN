from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('sconfpage/',views.sconfpage,name='sconfpage'),
    path('logout/', views.logout_request, name='logout'),
    # path('givedata/',views.givedata, name = 'givedata'),   example http end point
]