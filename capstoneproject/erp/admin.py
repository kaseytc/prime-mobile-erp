from django.contrib import admin
from erp.models import Accounts, Customers, Employees, Inventory, Invoices, Orders

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    model = Accounts
    list_display = ('username', 'acct_type', 'get_name')

    def get_name(self, obj):
        return obj.emp.fname + ' ' + obj.emp.lname
    get_name.short_description = 'Employee Name'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'dob')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'title' )


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'bin_bay', 'bin_aisle', 'inv_price', 'quantity')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'invoice_dt', 'pay_type', 'invoice_num', 'get_name')

    def get_name(self, obj):
        return obj.emp.fname + ' ' + obj.emp.lname
    get_name.short_description = 'Employee Name'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_dt', 'status', 'quantity', 'get_inventory', 'get_invoice')

    def get_inventory(self, obj):
        return obj.inventory.make + ' ' + obj.inventory.model
    get_inventory.short_description = 'Make & Model'

    def get_invoice(self, obj):
        return obj.invoice.invoice_id
    get_invoice.short_description = 'Invoice ID'


admin.site.register(Accounts, AccountAdmin)
admin.site.register(Customers, CustomerAdmin)
admin.site.register(Employees, EmployeeAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Invoices, InvoiceAdmin)
admin.site.register(Orders, OrderAdmin)


