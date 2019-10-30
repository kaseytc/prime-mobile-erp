from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index_sales', views.index_sales, name='index-sales'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('add_account/', views.add_account, name='add-account'),
    path('accounts/<pk>', views.AccountDetailView.as_view(), name='account-detail'),
    path('accounts/account_confirm_delete/<pk>', views.AccountDelete.as_view(), name='account-delete'),
    path('accounts/account_update/<pk>', views.AccountUpdate.as_view(), name='account-update'),

]

urlpatterns += [
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employee_form/', views.EmployeeCreate.as_view(), name='employee-form'),
    path('add_employee/', views.add_employee, name='add-employee'),
    path('employees/<pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/employee_confirm_delete/<pk>', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('employees/employee_update/<pk>', views.EmployeeUpdate.as_view(), name='employee-update'),
    # Search
    path('search_employee/', views.search_employee, name='search-employee-form'),
    path('search_employee_result/', views.SearchResultsView.as_view(), name='search-employee'),
    path('search_employee_result/employee_update/<pk>', views.EmployeeUpdate.as_view(), name='employee-update'),
]

urlpatterns += [
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('add_customer/', views.add_customer, name='add-customer'),
    path('customers/<pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/customer_confirm_delete/<pk>', views.CustomerDelete.as_view(), name='customer-delete'),
    path('customers/customer_update/<pk>', views.CustomerUpdate.as_view(), name='customer-update'),
]

urlpatterns += [
    path('add_order/', views.add_order, name='add-order'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/order_confirm_delete/<pk>', views.OrderDelete.as_view(), name='order-delete'),
    path('orders/order_update/<pk>', views.OrderUpdate.as_view(), name='order-update'),
]

urlpatterns += [
    path('inventories/', views.InventoryListView.as_view(), name='inventory-list'),
    path('add_inventory/', views.add_inventory, name='add-inventory'),
    path('inventories/<pk>', views.InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventories/inventory_confirm_delete/<pk>', views.InventoryDelete.as_view(), name='inventory-delete'),
    path('inventories/inventory_update/<pk>', views.InventoryUpdate.as_view(), name='inventory-update'),
]

urlpatterns += [
    path('add_invoice/', views.add_invoice, name='add-invoice'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<pk>', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/invoice_confirm_delete/<pk>', views.InvoiceDelete.as_view(), name='invoice-delete'),
    path('invoices/invoice_update/<pk>', views.InvoiceUpdate.as_view(), name='invoice-update')
]
