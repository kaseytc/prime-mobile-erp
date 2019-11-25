from django.contrib.auth.views import LoginView
from django.urls import path

from . import views, report

urlpatterns = [
    path('', views.index, name='index'),
    path('login', LoginView.as_view(template_name='login.html'), name='erp-login'),
    path('logout/', views.logout_view, name='erp-logout'),
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
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/order_confirm_cancel/<pk>', views.OrderCancel.as_view(), name='order-cancel'),
    path('orders/order_update/<pk>', views.OrderUpdate.as_view(), name='order-update'),
]

# Shopping
urlpatterns += [
    path('order_create/', views.OrderCreateView.as_view(), name='order-create'),
    path('product_list/', views.product_list, name='product-list'),
    path('add_item/', views.add_to_cart, name='add-item'),
    path('order_summary/', views.OrderSummaryView.as_view(), name='order-summary'),
]

# Invoice
urlpatterns += [
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<pk>', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    # path('invoices/invoice_confirm_delete/<pk>', views.InvoiceDelete.as_view(), name='invoice-delete'),
]

# Report
urlpatterns += [
    path('report/', report.index, name='report'),
    path('report/popular_phone/', report.popular_phone, name='popular-phone'),
    path('report/inventory_profits/', report.inventory_profits, name='inventory-profits'),
    path('report/employee_sales/', report.employee_sales, name='employee-sales'),
    path('report/customer_sales_table/', report.customer_sales_table, name='customer-sales-table'),
    path('report/customer_sales_graph/', report.customer_sales_table, name='customer-sales-graph'),
]


