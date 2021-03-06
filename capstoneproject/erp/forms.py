from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from .models import Customer, Employee, ErpUser, Inventory, Order, OrderDetail
from .models import ORDER_STATUS_CHOICES, PAY_TYPE_CHOICES, TITLE_TYPE_CHOICES


PAY_TYPE_EMPTY = [('', '---------')] + PAY_TYPE_CHOICES


class EmployeeForm(forms.Form):
    YEARS = [x for x in range(1950, 2010)]
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    title = forms.ChoiceField(widget=forms.RadioSelect, choices=TITLE_TYPE_CHOICES, required=True,)
    manager = forms.ModelChoiceField(queryset=Employee.objects.filter(title__in=["Manager", "Owner"]), required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
                                    required=True, label='Date of Birth',
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
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    title = forms.ChoiceField(widget=forms.RadioSelect, choices=TITLE_TYPE_CHOICES, required=True, )
    manager_emp = forms.ModelChoiceField(queryset=Employee.objects.filter(title__in=["Manager", "Owner"]),
                                         required=False, label='Manager')
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}))
    email = forms.EmailField(max_length=100, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex])

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
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
                                    required=True, label='Date of Birth',
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
    phone_regex = RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message="Enter a valid phone number")
    zip_regex = RegexValidator(regex='^\d{5}$', message="Enter a valid ZIP code")
    phone = forms.CharField(max_length=12, required=False, validators=[phone_regex],
                            widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}))
    email = forms.EmailField(max_length=100, required=False)
    zip = forms.CharField(max_length=5, required=False, validators=[zip_regex])

    class Meta:
        model = Customer
        fields = '__all__'
        labels = dict(fname=_('First Name'), lname=_('Last Name'), dob=_('Date of Birth'), addr1=_('Address Line 1'),
                      addr2=_('Address Line 2'), zip=_('ZIP Code'))
        exclude = ['dob', ]


class InventoryForm(forms.Form):
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


class OrderCreateForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.HiddenInput(), choices=ORDER_STATUS_CHOICES, required=True, initial='Create')
    emp = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Employee.objects.all(),
                                 label='Employee Name', required=True)
    cust = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Customer Name', required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.initial['status'] = 'Create'
        self.initial['emp'] = ErpUser.objects.get(pk=self.request.user.id).emp

    class Meta:
        model = Order
        fields = ['status', 'emp', 'cust',]


class OrderDetailForm(forms.ModelForm):

    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderUpdateForm(forms.ModelForm):
    emp = forms.ModelChoiceField(queryset=Employee.objects.all(), label='Employee', )
    pay_type = forms.ChoiceField(choices=PAY_TYPE_EMPTY, label='Payment Type', required=False)

    class Meta:
        model = Order
        fields = '__all__'







