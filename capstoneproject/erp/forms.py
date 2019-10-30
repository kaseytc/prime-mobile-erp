from django import forms
from .models import Account, Customer, Employee, Inventory, Invoice, Order
import datetime

'''
class EmployeeForm(forms.ModelForm):
    required_css_class = 'required'
    
    class Meta:
        model = Employee
        fields = '__all__'
'''


class EmployeeForm(forms.Form):
    TITLE_TYPE_CHOICES = [
        ('Manager', 'Manager'),
        ('Sales', 'Sales'),
    ]
    YEARS = [x for x in range(1950, 2010)]

    #required_css_class = 'required'
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    title = forms.ChoiceField(widget=forms.RadioSelect, choices=TITLE_TYPE_CHOICES, required=True,)
    manager = forms.ModelChoiceField(queryset=Employee.objects.filter(title__in=["Manager", "Owner"]), required=False)
    phone = forms.CharField(max_length=12, required=False)
    email = forms.EmailField(max_length=100, required=False)
    address_line_1 = forms.CharField(max_length=100, required=False)
    address_line_2 = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=2, required=False)
    zip = forms.CharField(max_length=5, required=False)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),
                                    required=False, initial=datetime.date.today)


class AccountForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Account
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Customer
        fields = '__all__'


class InventoryForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Inventory
        fields = '__all__'


class OrderForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Order
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    #required_css_class = 'required'

    class Meta:
        model = Invoice
        fields = '__all__'
