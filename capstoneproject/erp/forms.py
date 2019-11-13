from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import datetime

from .models import Customer, Employee, Inventory, Invoice, Order, ErpUser, OrderDetail

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


class EmployeeForm(forms.Form):
    YEARS = [x for x in range(1950, 2010)]
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    #required_css_class = 'required'
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    title = forms.ChoiceField(widget=forms.RadioSelect, choices=TITLE_TYPE_CHOICES, required=True,)
    manager = forms.ModelChoiceField(queryset=Employee.objects.filter(title__in=["Manager", "Owner"]), required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
                                    required=False, label='Date of Birth',
                                    help_text='DOB cannot be updated later')
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}))
    email = forms.EmailField(max_length=100, required=False)
    address_line_1 = forms.CharField(max_length=100, required=False, label='Address Line 1')
    address_line_2 = forms.CharField(max_length=50, required=False, label='Address Line 2')
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=2, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex], label='ZIP Code')


class EmployeeUpdateForm(forms.ModelForm):
    TITLE_TYPE_CHOICES = [
        ('Manager', 'Manager'),
        ('Sales', 'Sales'),
    ]
    #YEARS = [x for x in range(1950, 2010)]
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    title = forms.ChoiceField(widget=forms.RadioSelect, choices=TITLE_TYPE_CHOICES, required=True, )
    manager_emp = forms.ModelChoiceField(queryset=Employee.objects.filter(title__in=["Manager", "Owner"]),
                                         required=False, label='Manager')
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}))
    email = forms.EmailField(max_length=100, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex])
    #dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
    #                     required=False, label='Date of Birth')

    class Meta:
        model = Employee
        fields = '__all__'
        labels = dict(fname=_('First Name'), lname=_('Last Name'), dob=_('Date of Birth'),
                      addr1=_('Address Line 1'), addr2=_('Address Line 2'), zip=_('ZIP Code'))
        exclude = ['dob', ]


class CustomerForm(forms.Form):
    YEARS = [x for x in range(1910, 2020)]
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    #required_css_class = 'required'
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
                                    required=False, label='Date of Birth',
                                    help_text='DOB cannot be updated later')
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}),)
    email = forms.EmailField(max_length=100, required=False)
    address_line_1 = forms.CharField(max_length=100, required=False, label='Address Line 1')
    address_line_2 = forms.CharField(max_length=50, required=False, label='Address Line 2')
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=2, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex], label='ZIP Code')


class CustomerUpdateForm(forms.ModelForm):
    #YEARS = [x for x in range(1950, 2010)]
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}))
    email = forms.EmailField(max_length=100, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex])
    #dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
    #                     required=False, label='Date of Birth')

    class Meta:
        model = Customer
        fields = '__all__'
        labels = dict(fname=_('First Name'), lname=_('Last Name'), dob=_('Date of Birth'), addr1=_('Address Line 1'),
                      addr2=_('Address Line 2'), zip=_('ZIP Code'))
        exclude = ['dob', ]


class InventoryForm(forms.Form):
    #required_css_class = 'required'
    sku = forms.CharField(max_length=12, required=True, label='SKU')
    make = forms.CharField(max_length=50, required=True)
    model = forms.CharField(max_length=50, required=True)
    bin_aisle = forms.IntegerField(min_value=1, required=True, label='Bin Aisle')
    bin_bay = forms.IntegerField(min_value=1, required=True, label='Bin Bay')
    quantity = forms.IntegerField(min_value=0, required=True)
    cost = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        labels = dict(sku=_('SKU'), bin_aisle=_('Bin Aisle'), bin_bay=_('Bin Bay'), inv_cost=_('Cost'),
                      inv_price=_('Price'), inv_desc=_('Description'))

'''
class OrderForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Order
        fields = '__all__'
'''


class OrderForm(forms.ModelForm):
    #required_css_class = 'required'


    #cust = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True)
    #inventory = forms.ModelChoiceField(queryset=Inventory.objects.all(), required=True)
    #quantity = forms.IntegerField(min_value=0, required=True)
    #price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    status = forms.ChoiceField(widget=forms.RadioSelect, choices=STATUS_CHOICES, label='Order Status')
    pay_type = forms.ChoiceField(choices=PAY_TYPE_CHOICES, label='Payment Type')
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.all())

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['invoice', ]
        labels = dict(inventory=_('Inventory'), quantity=_('Quantity'), cust=_('Customer Name'))


class OrderUpdateForm(forms.ModelForm):
    #employee = Invoice.objects.last()

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['invoice', ]
        labels = dict(inventory=_('Inventory'), quantity=_('Quantity'), cust=_('Customer Name'))


class InvoiceForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Invoice
        fields = '__all__'


class OrderDetailForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderCreateForm(forms.ModelForm):
    cust = forms.CharField(max_length=50, required=True, label='Customer Name')
    class Meta:
        model = Order
        fields = ['cust', ]
        labels = dict(inventory=_('Inventory'), quantity=_('Quantity'), cust=_('Customer Name'))
        #fields = '__all__'


'''
order_id = models.AutoField(primary_key=True)
    order_dt = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS_CHOICES)
    cust = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    emp = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    #inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    #order_detail = models.ManyToManyField(OrderDetail)
    #quantity = models.PositiveIntegerField()
    #invoice = models.ForeignKey(Invoice, models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)
    
    detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    
    
    '''




