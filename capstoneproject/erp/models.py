# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _

TITLE_TYPE_CHOICES = [
    ('Manager', 'Manager'),
    ('Sales', 'Sales'),
]

STATUS_CHOICES = [
    ('Create', 'Create'),
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
]

PAY_TYPE_CHOICES = [
    ('Unpaid', 'Unpaid'),
    ('Cash', 'Cash'),
    ('VISA', 'VISA'),
    ('MasterCard', 'MasterCard'),
    ('AmEx', 'AmEx'),
]


class ErpUser(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE,  primary_key=True)
    emp = models.ForeignKey('Employee', models.DO_NOTHING)

    def __str__(self):
        return self.emp.fname + " " + self.emp.lname

    class Meta:
        managed = False
        db_table = 'ErpUser'
        verbose_name = 'ERP User'
        verbose_name_plural = 'ERP Users'


class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, blank=False, null=False)
    lname = models.CharField(max_length=50, blank=False, null=False)
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.fname + " " + self.lname

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.cust_id})

    class Meta:
        managed = False
        db_table = 'Customer'
        ordering = ['lname', 'fname', 'cust_id',]
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, blank=False, null=False)
    lname = models.CharField(max_length=50, blank=False, null=False)
    title = models.CharField(max_length=100, blank=False, null=False, choices=TITLE_TYPE_CHOICES)
    manager_emp = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    dob = models.DateField(blank=True, null=True, )
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.fname + " " + self.lname

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.emp_id})

    class Meta:
        managed = False
        db_table = 'Employee'
        ordering = ['title', 'lname', 'fname', 'emp_id', ]
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=12)
    make = models.CharField(max_length=50, blank=False, null=False)
    model = models.CharField(max_length=50, blank=False, null=False)
    bin_aisle = models.PositiveIntegerField()
    bin_bay = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    inv_cost = models.DecimalField(max_digits=10, decimal_places=2, )
    inv_price = models.DecimalField(max_digits=10, decimal_places=2,)
    inv_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.make + " " + self.model

    def get_absolute_url(self):
        return reverse('inventory-detail', kwargs={'pk': self.inventory_id})

    class Meta:
        managed = False
        db_table = 'Inventory'
        ordering = ['make', 'model',]
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_dt = models.DateTimeField(auto_now=True, auto_now_add=False)
    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)
    invoice_num = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2,)
    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS_CHOICES)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,)
    tax = models.DecimalField(max_digits=10, decimal_places=2,)
    cust = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return str(self.invoice_id)

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.invoice_id})

    class Meta:
        managed = False
        db_table = 'Invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

'''
class Invoice(models.Model):
    invoice_id = models.IntegerField(primary_key=True)
    invoice_dt = models.DateTimeField(blank=True, null=True)
    pay_type = models.CharField(max_length=10, blank=True, null=True)
    emp = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    invoice_num = models.IntegerField()
    total_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.CharField(max_length=-1, blank=True, null=True)
    grand_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    tax = models.TextField(blank=True, null=True)  # This field type is a guess.
    cust = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Invoice'
        '''


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_dt = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS_CHOICES)
    cust = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)

    def __str__(self):
        return str(self.order_id)

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.order_id})

    class Meta:
        managed = False
        db_table = 'Order'
        ordering=['status', 'order_id',]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    #inventory = models.OneToOneField(Inventory, on_delete=models.SET_NULL, null=True,)

    def __str__(self):
        return str(self.quantity) + " of " + self.inventory.make + self.inventory.model

    #def get_absolute_url(self):
        #return reverse('index', kwargs={'pk': self.detail_id})

    class Meta:
        managed = False
        db_table = 'Order_Detail'
        unique_together = (('order', 'inventory'),)
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'


'''
class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_dt = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    cust = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, blank=True, null=True)
    emp_id = models.IntegerField(blank=True, null=True)
    total_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    tax = models.TextField(blank=True, null=True)  # This field type is a guess.
    grand_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    pay_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Order'
'''

