from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import operator
from .models import Account, Customer, Employee, Inventory, Invoice, Order
from .forms import AccountForm, CustomerForm, EmployeeForm, InventoryForm, OrderForm, InvoiceForm


# Create your views here.


def index(request):
    return render(request, 'index.html', locals())


def index_sales(request):
    return render(request, 'index_sales.html', locals())


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
    return render(request, 'employee/add_employee.html', {'form': form, 'submitted': submitted})


class EmployeeCreate(CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee-list')


class EmployeeListView(generic.ListView):
    model = Employee
    queryset = Employee.objects.all()
    template_name = 'employee/employee_list.html'
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    return context


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['now'] = timezone.now()
#        return context


'''
def employee_detail_view(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    return render(request, 'employee_detail.html', context={'employee': employee})
'''


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')


class EmployeeUpdate(UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'employee/employee_update_form.html'
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
    return render(request, 'customer/add_customer.html', {'form': form, 'submitted': submitted})


class CustomerListView(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/customer_list.html'


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')


class CustomerUpdate(UpdateView):
    model = Customer
    fields = '__all__'
    template_name = 'customer/customer_update_form.html'





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
    return render(request, 'account/add_account.html', {'form': form, 'submitted': submitted})


class AccountListView(generic.ListView):
    model = Account
    queryset = Account.objects.all()
    template_name = 'account/account_list.html'


class AccountDetailView(generic.DetailView):
    model = Account
    template_name = 'account/account_detail.html'


class AccountDelete(DeleteView):
    model = Account
    template_name = 'account/account_confirm_delete.html'
    success_url = reverse_lazy('account-list')


class AccountUpdate(UpdateView):
    model = Account
    fields = '__all__'
    template_name = 'account/account_update_form.html'





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
    return render(request, 'inventory/add_inventory.html', {'form': form, 'submitted': submitted})


class InventoryListView(generic.ListView):
    model = Inventory
    queryset = Inventory.objects.all()
    template_name = 'inventory/inventory_list.html'


class InventoryDetailView(generic.DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'


class InventoryDelete(DeleteView):
    model = Inventory
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')


class InventoryUpdate(UpdateView):
    model = Inventory
    fields = '__all__'
    template_name = 'inventory/inventory_update_form.html'





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
    return render(request, 'order/add_order.html', {'form': form, 'submitted': submitted})


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/order_detail.html'


class OrderDelete(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order-list')


class OrderUpdate(UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'order/order_update_form.html'
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
    return render(request, 'invoice/add_invoice.html', {'form': form, 'submitted': submitted})


class InvoiceListView(generic.ListView):
    model = Invoice
    queryset = Invoice.objects.all()
    template_name = 'invoice/invoice_list.html'


class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'invoice/invoice_detail.html'


class InvoiceDelete(DeleteView):
    model = Invoice
    template_name = 'invoice/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice-list')


class InvoiceUpdate(UpdateView):
    model = Invoice
    fields = '__all__'
    template_name = 'invoice/invoice_update_form.html'


'''
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
'''


def search_employee(request):
    return render(request, 'employee/search_employee.html', locals())


class SearchResultsView(EmployeeListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    #queryset = Employee.objects.filter(title__icontains='Manager')

    def get_queryset(self):  # new
        #query = self.request.GET.get('title')
        title = self.request.GET.get('title')
        fname = self.request.GET.get('fname')
        lname = self.request.GET.get('lname')

        #if fname is not None:
        #    object_list = Employee.objects.filter(fname__icontains=fname)

        object_list = Employee.objects.filter(
            Q(title__icontains=title) |
            Q(fname__icontains=fname) |
            Q(lname__icontains=lname)
        )
        #or_lookup = (
        #    Q(title__icontains=title) |
        #    Q(fname__icontains=fname) |
        #    Q(lname__icontains=lname)
        #)
        #object_list =
        return object_list



'''
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
'''