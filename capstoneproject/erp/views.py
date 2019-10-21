from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from django.http import HttpResponseRedirect

from django .views import generic

from erp.models import Employee
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ERP index.")


def home(request):
    return render(request, 'home.html', locals())

#???
class EmployeeListView(generic.ListView):
    model = Employee



def listAllEmployee(request):

    employees = Employee.objects.all().order_by('emp_id')
    return render(request,'listAllEmployee.html', locals())

def searchEmployee(request):
    return render(request, 'searchEmployee.html', locals())



def base(request):
    return render(request, 'base.html', locals())

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['title', 'fname', 'lname', 'phone', 'email',
                  'addr1', 'addr2', 'city', 'state', 'zip', 'dob', 'manager_emp',]


def createEmployee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save()
            return HttpResponseRedirect('../listAllEmployee/')
           # return HttpResponseRedirect('../')

    form = EmployeeForm()
    return render(request, 'create_employee.html', {'form': form})



