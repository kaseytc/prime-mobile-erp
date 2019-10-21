from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('listall/', views.listall, name='listall'),
    path('', views.home, name='home'),
    path('listAllEmployee/', views.listAllEmployee),
    path('searchEmployee/', views.searchEmployee),
    path('base/', views.base),
    path('createEmployee/', views.createEmployee), #OK
    path('employees/', views.EmployeeListView.as_view(), name='employees'),
]
