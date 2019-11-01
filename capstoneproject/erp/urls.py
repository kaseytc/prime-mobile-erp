from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='erp-login'),
    path('logout/', views.logout_view, name='erp-logout'),
]

# Django authentication urls (login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# Account
urlpatterns += [
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('add_account/', views.add_account, name='add-account'),
    path('accounts/<pk>', views.AccountDetailView.as_view(), name='account-detail'),
    path('accounts/account_confirm_delete/<pk>', views.AccountDelete.as_view(), name='account-delete'),
    path('accounts/account_update/<pk>', views.AccountUpdate.as_view(), name='account-update'),

]

# Employee
urlpatterns += [
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('add_employee/', views.add_employee, name='add-employee'),
    path('employees/<pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/employee_confirm_delete/<pk>', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employees/employee_update/<pk>', views.EmployeeUpdate.as_view(), name='employee-update'),
    path('search_employee/', views.search_employee, name='search-employee-form'),
    path('search_employee_result/', views.EmployeeSearchResultsView.as_view(), name='search-employee-result'),
]

# Customer
urlpatterns += [
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('add_customer/', views.add_customer, name='add-customer'),
    path('customers/<pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/customer_confirm_delete/<pk>', views.CustomerDelete.as_view(), name='customer-delete'),
    path('customers/customer_update/<pk>', views.CustomerUpdate.as_view(), name='customer-update'),
    path('search_customer/', views.search_customer, name='search-customer-form'),
    path('search_customer_result/', views.CustomerSearchResultsView.as_view(), name='search-customer-result'),
]

# Inventory
urlpatterns += [
    path('inventories/', views.InventoryListView.as_view(), name='inventory-list'),
    path('add_inventory/', views.add_inventory, name='add-inventory'),
    path('inventories/<pk>', views.InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/inventory_confirm_delete/<pk>', views.InventoryDelete.as_view(), name='inventory-delete'),
    path('inventories/inventory_update/<pk>', views.InventoryUpdate.as_view(), name='inventory-update'),
    path('search_inventory/', views.search_inventory, name='search-inventory-form'),
    path('search_inventory_result/', views.InventorySearchResultsView.as_view(), name='search-inventory-result'),
]

# Order
urlpatterns += [
    path('add_order/', views.add_order, name='add-order'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/order_confirm_delete/<pk>', views.OrderDelete.as_view(), name='order-delete'),
    path('orders/order_update/<pk>', views.OrderUpdate.as_view(), name='order-update'),
]

# Invoice
urlpatterns += [
    path('add_invoice/', views.add_invoice, name='add-invoice'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<pk>', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/invoice_confirm_delete/<pk>', views.InvoiceDelete.as_view(), name='invoice-delete'),
    path('invoices/invoice_update/<pk>', views.InvoiceUpdate.as_view(), name='invoice-update')
]
