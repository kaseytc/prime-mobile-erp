# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# User = get_user_model()

TITLE_TYPE_CHOICES = [
    ('Manager', 'Manager'),
    ('Sales', 'Sales'),
]

STATUS_CHOICES = [
    ('Complete', 'Complete'),
    ('Pending', 'Pending'),
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

    #def delete(self, using=None, keep_parents=False):
       # self.

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
    cust = models.ForeignKey(Customer, models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING)
    emp_id = models.ForeignKey(Employee, models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,)
    tax = models.DecimalField(max_digits=10, decimal_places=2,)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,)
    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)

    def __unicode__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.order_id})

    class Meta:
        managed = False
        db_table = 'Order'
        ordering=['status', 'order_id',]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

'''class Order(models.Model):
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


class OrderDetail(models.Model):
    order_id = models.IntegerField(primary_key=True)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING, blank=True, null=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'Order_Detail'
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



