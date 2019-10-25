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
        fName = cleaned_data.get("fname")
        lName = cleaned_data.get("lname")
        if not (fName and lName):
            raise forms.ValidationError("You must enter First Name and Last Name.")
