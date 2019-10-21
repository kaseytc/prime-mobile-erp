from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('add_employee/', views.add_employee, name='add-employee'),
    path('listAllEmployee/', views.listAllEmployee),
    path('searchEmployee/', views.searchEmployee),
    path('employees/', views.EmployeeListView.as_view(), name='employees'),
]
