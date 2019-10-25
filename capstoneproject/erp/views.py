from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django .views import generic
from .models import Employee
from .forms import EmployeeForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
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


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['now'] = timezone.now()
#        return context


'''
def employee_detail_view(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    return render(request, 'employee_detail.html', context={'employee': employee})
'''

def searchEmployee(request):
    return render(request, 'searchEmployee.html', locals())


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

class EmployeeUpdate(UpdateView):
    model = Employee
    fields = ['fname', 'lname']
    #template_name = 'employee_update_form.html'
    template_name_suffix = '_update_form'

