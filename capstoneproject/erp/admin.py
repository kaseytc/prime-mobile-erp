from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Customer, Employee, Inventory, Invoice, Order, OrderDetail
from .models import ErpUser

# Register your models here.

# Define an inline admin descriptor for ErpUser model
# which acts a bit like a singleton


class ErpUserInline(admin.StackedInline):
    model = ErpUser
    can_delete = False
    verbose_name_plural = 'erpuser'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ErpUserInline,)
    list_display = ('username', 'first_name', 'last_name',  'is_superuser',  'is_staff', 'last_login',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname')
    search_fields = ('fname', 'lname')
    ordering = ('cust_id',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'title')
    search_fields = ('title','fname', 'lname')
    ordering = ('emp_id',)
    list_filter = ('title',)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'bin_bay', 'bin_aisle', 'inv_price', 'quantity')
    search_fields = ('make',)
    ordering = ('inventory_id',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'invoice_dt', 'pay_type', 'invoice_num', 'get_name')
    search_fields = ('invoice_id', 'invoice_dt')
    ordering = ('invoice_id',)

    def get_name(self, obj):
        return obj.emp.fname + ' ' + obj.emp.lname
    get_name.short_description = 'Employee Name'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_dt', 'status', 'get_invoice')
    search_fields = ('order_id', 'order_dt')
    ordering = ('order_id',)
    list_filter = ('status',)

    def get_invoice(self, obj):
        return obj.invoice.invoice_id
    get_invoice.short_description = 'Invoice ID'


class OrderDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

