from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django .views import generic
from .models import Account, Customer, Employee, Inventory, Invoice, Order
from .forms import AccountForm, CustomerForm, EmployeeForm, InventoryForm
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
    fields = '__all__'
    template_name = 'employee_update_form.html'
    #template_name_suffix = '_update_form'




def add_customer(request):
    submitted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = CustomerForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_customer.html', {'form': form, 'submitted': submitted})

class CustomerListView(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer_list.html'
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'customer_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['now'] = timezone.now()
#        return context


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

class CustomerUpdate(UpdateView):
    model = Customer
    fields = '__all__'
    template_name = 'customer_update_form.html'
    #template_name_suffix = '_update_form'




def add_account(request):
    submitted = False
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = AccountForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_account.html', {'form': form, 'submitted': submitted})


class AccountListView(generic.ListView):
    model = Account
    queryset = Account.objects.all()
    template_name = 'account_list.html'
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'account_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['now'] = timezone.now()
#        return context


class AccountDelete(DeleteView):
    model = Account
    template_name = 'account_confirm_delete.html'
    success_url = reverse_lazy('account-list')


class AccountUpdate(UpdateView):
    model = Account
    fields = '__all__'
    template_name = 'account_update_form.html'
    #template_name_suffix = '_update_form'




def add_inventory(request):
    submitted = False
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = InventoryForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_inventory.html', {'form': form, 'submitted': submitted})


class InventoryListView(generic.ListView):
    model = Inventory
    queryset = Inventory.objects.all()
    template_name = 'inventory_list.html'
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


class InventoryDetailView(generic.DetailView):
    model = Inventory
    template_name = 'inventory_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['now'] = timezone.now()
#        return context


class InventoryDelete(DeleteView):
    model = Inventory
    template_name = 'inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')


class InventoryUpdate(UpdateView):
    model = Inventory
    fields = '__all__'
    template_name = 'inventory_update_form.html'
    #template_name_suffix = '_update_form'