from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django .views import generic
from .models import Employee
from .forms import EmployeeForm
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ERP index.")


def home(request):
    return render(request, 'home.html', locals())


def add_employee(request):
    submitted = False
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = EmployeeForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_employee.html', {'form': form, 'submitted': submitted})


class EmployeeListView(generic.ListView):
    model = Employee
    queryset = Employee.objects.all()
    template_name = 'employee_list.html'
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


class EmployeeDetailView(generic.DeleteView):
    model = Employee


def searchEmployee(request):
    return render(request, 'searchEmployee.html', locals())

