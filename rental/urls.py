from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = 'rental'

urlpatterns = [
    # ex: /getdata/
    #path('', views.home, name='index'),
    # ex: /getdata/select/
    path('', views.input, name='input'),
  
    
]
