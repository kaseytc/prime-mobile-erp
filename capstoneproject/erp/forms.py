from django import forms
from .models import Account, Customer, Employee, Inventory, Invoice, Order


class EmployeeForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Employee
        fields = '__all__'


class AccountForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Account
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Customer
        fields = '__all__'


class InventoryForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Inventory
        fields = '__all__'


class OrderForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Order
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    # required_css_class = 'required'
    class Meta:
        model = Invoice
        fields = '__all__'
