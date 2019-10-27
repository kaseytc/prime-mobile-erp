from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django .views import generic
from .models import Account, Customer, Employee, Inventory, Invoice, Order
from .forms import AccountForm, CustomerForm, EmployeeForm, InventoryForm, OrderForm, InvoiceForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
import operator
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ERP index.")


def home(request):
    return render(request, 'home.html', locals())

@permission_required('can add employee')
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





class EmployeeDelete(PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')
    permission_required= 'change_post'


class EmployeeUpdate(PermissionRequiredMixin,UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'employee_update_form.html'
    permission_required = 'change_post'
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



class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'customer_detail.html'



class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

class CustomerUpdate(UpdateView):
    model = Customer
    fields = '__all__'
    template_name = 'customer_update_form.html'




@permission_required('can add account')
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



class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'account_detail.html'



class AccountDelete(DeleteView):
    model = Account
    template_name = 'account_confirm_delete.html'
    success_url = reverse_lazy('account-list')


class AccountUpdate(UpdateView):
    model = Account
    fields = '__all__'
    template_name = 'account_update_form.html'





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



class InventoryDetailView(generic.DetailView):
    model = Inventory
    template_name = 'inventory_detail.html'



class InventoryDelete(DeleteView):
    model = Inventory
    template_name = 'inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')


class InventoryUpdate(UpdateView):
    model = Inventory
    fields = '__all__'
    template_name = 'inventory_update_form.html'





def add_order(request):
    submitted = False
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = OrderForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_order.html', {'form': form, 'submitted': submitted})


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'order_list.html'



class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'



class OrderDelete(DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order-list')


class OrderUpdate(UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'order_update_form.html'
    #template_name_suffix = '_update_form'



def add_invoice(request):
    submitted = False
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = InvoiceForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_invoice.html', {'form': form, 'submitted': submitted})


class InvoiceListView(generic.ListView):
    model = Invoice
    queryset = Invoice.objects.all()
    template_name = 'invoice_list.html'



class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'



class InvoiceDelete(DeleteView):
    model = Invoice
    template_name = 'invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice-list')


class InvoiceUpdate(UpdateView):
    model = Invoice
    fields = '__all__'
    template_name = 'invoice_update_form.html'



class ＥmployeeSearchListView(EmployeeListView):
    """
    Display a Employee List page filtered by the search query.
    """
    #paginate_by = 10

    def get_queryset(self):
        result = super(ＥmployeeSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Employee(lname__icontains=lname) for lname in query_list)) |
                reduce(operator.and_,
                       (Employee(fname__icontains=fname) for fname in query_list)) |
                reduce(operator.and_,
                   (Employee(title__icontains=title) for title in query_list))
            )

        return result


def search_employee(request):
    return render(request, 'search_employee.html', locals())


class SearchResultsView(EmployeeListView):
    model = Employee
    template_name = 'employee_list.html'
    #queryset = Employee.objects.filter(title__icontains='Manager')

    def get_queryset(self):  # new
        query = self.request.GET.get('title')
        object_list = Employee.objects.filter(title__icontains=query)
            #Employee(title__icontains=query)
            #| Employee(state__icontains=query)
        #)
        return object_list

