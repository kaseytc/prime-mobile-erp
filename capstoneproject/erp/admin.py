from django.contrib import admin

# Register your models here.
from erp.models import Accounts, Customers, Employees, Inventory, Invoices, Orders

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'inv_price', 'quantity')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'fname', 'lname', 'title' )


admin.site.register(Accounts)
admin.site.register(Customers)
admin.site.register(Employees, EmployeeAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Invoices)
admin.site.register(Orders)


