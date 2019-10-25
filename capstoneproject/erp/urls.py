from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('add_employee/', views.add_employee, name='add-employee'),
    #path('add_employee/', views.EmployeeCreateView.as_view(), name='add-employee'),
    path('searchEmployee/', views.searchEmployee),
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/<pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    #path('employees/<int:emp_id>', views.employee_detail_view, name='employee-detail'),
    path('employees/employee_confirm_delete/<pk>', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employees/employee_update/<pk>', views.EmployeeDelete.as_view(), name='employee-update'),
]
