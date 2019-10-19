from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('listall/', views.listall, name='listall'),
    path('', views.home, name='home'),
    path('listall/', views.listall),
]
