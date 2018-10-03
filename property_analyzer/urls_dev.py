"""property_analyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from property_analyzer.forms import LoginForm
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

urlpatterns = [
    path('property_analyzer', TemplateView.as_view(template_name='home.html'),name="home"),
    path('property_analyzer/admin/', admin.site.urls),
    path('property_analyzer/rental/', include('rental.urls')),
    path('property_analyzer/iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
    path('property_analyzer/login/', login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'), # not sure why i had to remove name='login' here???
    path('property_analyzer/logout/', logout, name='logout'),      
]
