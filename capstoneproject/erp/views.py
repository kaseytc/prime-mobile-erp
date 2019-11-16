from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import operator
from django.http import Http404
from django.db.models import F

from .models import Customer, Employee, Inventory, Invoice, Order, ErpUser, OrderDetail
from .forms import CustomerForm, EmployeeForm, InventoryForm, OrderForm, \
    EmployeeUpdateForm, CustomerUpdateForm, InventoryUpdateForm, InvoiceForm, OrderUpdateForm, \
    OrderDetailForm, OrderCreateForm

# Create your views here.

invoice_num = 1


def index(request):
    return render(request, 'index.html', locals())


def logout_view(request):
    # Redirect to a success page.
    try:
        current_user = request.user
        if current_user.first_name != "":
            name = current_user.first_name
        else:
            name = current_user.username
    except AttributeError:
        name = ""
    logout(request)
    return render(request, 'logout.html', locals())


# @permission_required('can add employee')
def add_employee(request):
    submitted = False
    inserted = False
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            manager_emp = form.cleaned_data.get('manager_employee_id')
            title = form.cleaned_data.get('title')
            addr1 = form.cleaned_data.get('address_line_1')
            addr2 = form.cleaned_data.get('address_line_2')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            dob = form.cleaned_data.get('date_of_birth')
            p = Employee(
                fname=fname, lname=lname, phone=phone, email=email,
                manager_emp=manager_emp, title=title, addr1=addr1, addr2=addr2 ,
                city=city, state=state, zip=zip, dob=dob,
            )
            while inserted is False:
                try:
                    p.save()
                    inserted = True
                except IntegrityError:
                    pass
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = EmployeeForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'employee/add_employee.html', {'form': form, 'submitted': submitted})


class EmployeeListView(generic.ListView):
    model = Employee
    queryset = Employee.objects.all()
    template_name = 'employee/employee_list.html'
    paginate_by = 25


class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'


# @permission_required('Can delete employee')
class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object(*args)
        user_account_id = None
        # delete ErpUser data
        try:
            user_account_id = ErpUser.objects.get(emp=self.object.emp_id).account_id
            ErpUser.objects.get(emp=self.object.emp_id).delete()
        except ErpUser.DoesNotExist:
            print("ErpUser does not exist")
        # delete user account
        try:
            User.objects.get(pk=user_account_id).delete()
        except User.DoesNotExist:
            print("User does not exist")
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


# @permission_required('Can change employee')
class EmployeeUpdate(UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'employee/employee_update_form.html'


def search_employee(request):
    return render(request, 'employee/employee_search.html', locals())


# class SearchResultsView(EmployeeListView):
class EmployeeSearchResultsView(generic.ListView):
    template_name = 'employee/employee_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = list()
        if query is not None:
            query_list = query.split()
            for q in query_list:
                object_list += Employee.objects.filter(
                    Q(title__icontains=q) |
                    Q(fname__icontains=q) |
                    Q(lname__icontains=q)
                )
        return object_list


def add_customer(request):
    submitted = False
    inserted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            addr1 = form.cleaned_data.get('address_line_1')
            addr2 = form.cleaned_data.get('address_line_2')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            dob = form.cleaned_data.get('date_of_birth')
            p = Customer(
                fname=fname, lname=lname, phone=phone, email=email, addr1=addr1,
                addr2=addr2, city=city, state=state, zip=zip, dob=dob,
            )
            while inserted is False:
                try:
                    p.save()
                    inserted = True
                except IntegrityError:
                    pass
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
    paginate_by = 25


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')


class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'customer/customer_update_form.html'


def search_customer(request):
    return render(request, 'customer/customer_search.html', locals())


class CustomerSearchResultsView(generic.ListView):
    template_name = 'customer/customer_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = list()

        if query is not None:
            query_list = query.split()
            for q in query_list:
                object_list += Customer.objects.filter(
                    Q(fname__icontains=q) |
                    Q(lname__icontains=q)
                )

        return object_list


def add_inventory(request):
    submitted = False
    inserted = False
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            sku = form.cleaned_data.get('sku')
            make = form.cleaned_data.get('make')
            model = form.cleaned_data.get('model')
            inv_desc = form.cleaned_data.get('description')
            inv_price = form.cleaned_data.get('price')
            inv_cost = form.cleaned_data.get('cost')
            quantity = form.cleaned_data.get('quantity')
            bin_aisle = form.cleaned_data.get('bin_aisle')
            bin_bay = form.cleaned_data.get('bin_bay')
            p = Inventory(
                sku=sku, make=make, model=model, inv_desc=inv_desc, inv_price=inv_price,
                inv_cost=inv_cost, quantity=quantity, bin_aisle=bin_aisle, bin_bay=bin_bay,
            )
            while inserted is False:
                try:
                    p.save()
                    inserted = True
                except IntegrityError:
                    pass
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
    paginate_by = 25


class InventoryDetailView(generic.DetailView):
    model = Inventory
    template_name = 'inventory/inventory_detail.html'


class InventoryDelete(DeleteView):
    model = Inventory
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')


class InventoryUpdate(UpdateView):
    model = Inventory
    form_class = InventoryUpdateForm
    template_name = 'inventory/inventory_update_form.html'


def search_inventory(request):
    return render(request, 'inventory/inventory_search.html', locals())


class InventorySearchResultsView(generic.ListView):
    template_name = 'inventory/inventory_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = list()
        if query is not None:
            query_list = query.split()
            for q in query_list:
                object_list = Inventory.objects.filter(
                    Q(make__icontains=q) |
                    Q(model__icontains=q)
                )
        return object_list


# TODO: the ability to charge tax on an order. create, mark an invoice as paid when payment has been taken. \
#  remove and store invoices for customers. assign and remove employees on an order.
def add_order(request):
    global invoice_num
    submitted = False
    inserted_o = False
    inserted_i = False
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get('status')
            cust = form.cleaned_data.get('cust')
            inventory = form.cleaned_data.get('inventory')
            quantity = form.cleaned_data.get('quantity')
            #invoice = form.cleaned_data.get('invoice')
            pay_type = form.cleaned_data.get('pay_type')
            #price = form.cleaned_data.get('price')

            new_invoice = Invoice(pay_type=pay_type, invoice_num=invoice_num,
                                  emp=ErpUser.objects.get(pk=request.user.id).emp)
            while inserted_i is False:
                try:
                    new_invoice.save()
                    inserted_i = True
                except IntegrityError:
                    pass
            invoice_num += 1
            latest_invoice_num = Invoice.objects.last()

            new_order = Order(status=status, cust=cust, inventory=inventory, quantity=quantity,
                              invoice=latest_invoice_num)
            while inserted_o is False:
                try:
                    new_order.save()
                    inserted_o = True
                except IntegrityError:
                    pass
            return HttpResponseRedirect('./?submitted=True')
    else:
        form = OrderForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'order/add_order.html', {'form': form, 'submitted': submitted})


''' 
     STATUS_CHOICES = [
        ('Complete', 'Complete'),
        ('Pending', 'Pending'),
    ]
    order_id = models.AutoField(primary_key=True)
    order_dt = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, choices=STATUS_CHOICES)
    cust = models.ForeignKey(Customer, models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING)
    
    PAY_TYPE_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Cash', 'Cash'),
        ('VISA', 'VISA'),
        ('MasterCard', 'MasterCard'),
        ('AmEx', 'AmEx'),
    ]
    invoice_id = models.AutoField(primary_key=True)
    invoice_dt = models.DateTimeField(auto_now=True, auto_now_add=False)
    pay_type = models.CharField(max_length=10, blank=True, null=True, choices=PAY_TYPE_CHOICES)
    emp = models.ForeignKey(Employee, models.DO_NOTHING)
    invoice_num = models.IntegerField()
'''


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'
    paginate_by = 25


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/order_detail.html'


class OrderDelete(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order-list')


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'order/order_update_form.html'


def add_invoice(request):
    submitted = False
    inserted = False
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            while inserted is False:
                try:
                    form.save()
                    inserted = True
                except IntegrityError:
                    pass
            return HttpResponseRedirect('./?submitted=""True')
    else:
        form = InvoiceForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'invoice/add_invoice.html', {'form': form, 'submitted': submitted})


class InvoiceListView(generic.ListView):
    model = Invoice
    queryset = Invoice.objects.all()
    template_name = 'invoice/invoice_list.html'
    paginate_by = 25


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


# class OrderItemView(CreateView):
#    model = OrderDetail
#    form_class = OrderDetailForm
#    template_name = 'shopping/order_item.html'
#   success_url = reverse_lazy('order-list')


# NewOrder
# TODO: the ability to charge tax on an order. create, mark an invoice as paid when payment has been taken. \
#  remove and store invoices for customers. assign and remove employees on an order.
class OrderCreateView(CreateView):
    # global new_order
    model = Order
    form_class = OrderCreateForm
    template_name = 'shopping/order_step_1_create.html'
    success_url = reverse_lazy('product-list')

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs

    # def get_success_url(self, **kwargs):
    #    # obj = form.instance or self.object
    #    return reverse_lazy("orders", kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #    self.object = form.save()
    #   new_order = self.object
    #   print(new_order.order_id)
    #    return HttpResponseRedirect(self.get_success_url())


def product_list(request):
    object_list = Inventory.objects.all()
    context = {
        'object_list': object_list,
    }

    return render(request, "shopping/order_step_2_detail.html", context)


def add_to_cart(request):
    inserted = False
    if request.method == 'POST':
        if request.POST.get('quantity') and request.POST.get('inventory'):
            order_detail = OrderDetail()
            order_detail.order = Order.objects.latest('order_dt')
            inventory_id = request.POST.get('inventory')
            order_detail.inventory = Inventory.objects.get(pk=inventory_id)
            order_detail.quantity = request.POST.get('quantity')

            while inserted is False:
                try:
                    order_detail.save()
                    inserted = True
                except IntegrityError:
                    query = OrderDetail.objects.filter(inventory=order_detail.inventory, order=order_detail.order)
                    query.update(quantity=F('quantity') + order_detail.quantity)
                    # print(query)
                    # print('IntegrityError')
                    break
            # return HttpResponseRedirect('./?submitted=True')
            # return render(request, 'shopping/order_step_2_detail.html')
            return redirect('order-summary')


class OrderSummaryView(generic.ListView):
    model = OrderDetail
    form_class = OrderDetailForm
    order_id = Order.objects.latest('order_dt')
    queryset = OrderDetail.objects.filter(order=order_id)
    template_name = 'shopping/order_step_3_summary.html'


# def order_summary(request):



