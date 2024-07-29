"""
URL configuration for VoyageProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# VoyageProj/urls.py

from django.contrib import admin
from django.urls import path
from VoyageApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('results/<int:pk>/', views.results, name='results'),

  path('place_info/<int:pk>/', views.place_info, name='place_info')
# path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
]





