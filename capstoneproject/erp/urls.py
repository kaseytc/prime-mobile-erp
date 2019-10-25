from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    #path('add_employee/', views.EmployeeCreateView.as_view(), name='add-employee'),
    path('searchEmployee/', views.searchEmployee),
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('add_employee/', views.add_employee, name='add-employee'),
    path('employees/<pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    #path('employees/<int:emp_id>', views.employee_detail_view, name='employee-detail'),
    path('employees/employee_confirm_delete/<pk>', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employees/employee_update/<pk>', views.EmployeeUpdate.as_view(), name='employee-update'),
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('add_account/', views.add_account, name='add-account'),
    path('accounts/<pk>', views.AccountDetailView.as_view(), name='account-detail'),
    path('accounts/account_confirm_delete/<pk>', views.AccountDelete.as_view(), name='account-delete'),
    path('accounts/account_update/<pk>', views.AccountUpdate.as_view(), name='account-update'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('add_customer/', views.add_customer, name='add-customer'),
    path('customers/<pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/customer_confirm_delete/<pk>', views.CustomerDelete.as_view(), name='customer-delete'),
    path('customers/customer_update/<pk>', views.CustomerUpdate.as_view(), name='customer-update'),
    path('inventories/', views.InventoryListView.as_view(), name='inventory-list'),
    path('add_inventory/', views.add_inventory, name='add-inventory'),
    path('inventories/<pk>', views.InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/inventory_confirm_delete/<pk>', views.InventoryDelete.as_view(), name='inventory-delete'),
    path('inventories/inventory_update/<pk>', views.InventoryUpdate.as_view(), name='inventory-update'),
]
