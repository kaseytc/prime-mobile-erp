from django import forms
from .models import Account, Customer, Employee, Inventory, Invoice, Order


class EmployeeForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Employee
        fields = '__all__'
        #'manager_emp'

    def clean(self):
        cleaned_data = super().clean()
        fname = cleaned_data.get("fname")
        lname = cleaned_data.get("lname")
        title = cleaned_data.get("title")
        if not (fname and lname and title):
            raise forms.ValidationError("You must enter First Name, Last Name and Title.")


class AccountForm(forms.ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = Account
        fields = '__all__'
        #exclude = ['emp',]

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        pwd = cleaned_data.get("pwd")
        if not (username and pwd):
            raise forms.ValidationError("You must enter username and password.")


class CustomerForm(forms.ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = Customer
        fields = '__all__'
        #'manager_emp'

    def clean(self):
        cleaned_data = super().clean()
        fname = cleaned_data.get("fname")
        lname = cleaned_data.get("lname")
        if not (fname and lname):
            raise forms.ValidationError("You must enter First Name and Last Name.")


class InventoryForm(forms.ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = Inventory
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        make = cleaned_data.get("make")
        model = cleaned_data.get("model")
        if not (make and model):
            raise forms.ValidationError("You must enter Make and Model.")


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
