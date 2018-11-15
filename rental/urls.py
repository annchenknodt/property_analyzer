from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = 'rental'

urlpatterns = [
    # ex: /getdata/
    path('', views.index, name='index'),
    # ex: /getdata/select/
       # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    path('<int:analysis_id>/results/', views.results, name='results'),
  	path('<int:analysis_id>/edit/', views.edit, name='edit'),
    
]
