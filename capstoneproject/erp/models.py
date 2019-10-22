# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    acct_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    pwd = models.CharField(max_length=100, blank=True, null=True)

    ACCT_TYPE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('STD', 'Standard'),
    ]

    acct_type = models.CharField(max_length=20, blank=True, null=True, choices=ACCT_TYPE_CHOICES)
    #acct_type = models.CharField(max_length=20, blank=True, null=True,)
    emp = models.ForeignKey('Employee', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Account'


class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    manager_emp = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    TITLE_TYPE_CHOICES = [
        ('M', 'Manager'),
        ('S', 'Sales'),
    ]

    title = models.CharField(max_length=100, blank=True, null=True, choices=TITLE_TYPE_CHOICES)
    #title = models.CharField(max_length=100, blank=True, null=True)
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee'
        ordering = ['title', 'lname',]


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=12)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    inv_desc = models.TextField(blank=True, null=True)
    inv_price = models.DecimalField(max_digits=10, decimal_places=2)
    inv_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    bin_aisle = models.PositiveIntegerField()
    bin_bay = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'Inventory'


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_dt = models.DateTimeField()

    PAY_TYPE_CHOICES= [
        ('CA', 'Cash'),
        ('CR', 'Credit'),
    ]

    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)
    #pay_type = models.CharField(max_length=10, blank=True, null=True,)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)
    invoice_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Invoice'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_dt = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES= [
        ('C', 'Complete'),
        ('P', 'Pending'),
    ]

    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS_CHOICES)
    #status = models.CharField(max_length=20, blank=True, null=True)
    cust = models.ForeignKey(Customer, models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING)
    #emp = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Order'


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
