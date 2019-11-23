from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import operator
from django.http import Http404
from django.http import JsonResponse
from django.template import RequestContext
from decimal import Decimal
from money.currency import Currency
from money.money import Money
from re import sub

from .models import Customer, Employee, ErpUser, Inventory, Invoice, Order, OrderDetail
from .forms import CustomerForm, EmployeeForm, InventoryForm, OrderCreateForm, OrderDetailForm
from .forms import EmployeeUpdateForm, CustomerUpdateForm, InventoryUpdateForm, OrderUpdateForm

import datetime
import locale

# Create your views here.

SALES_TAX_RATE = 0.089


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


@permission_required('can add employee')
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


class EmployeeDelete(PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')
    permission_required = 'change_post'

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


class EmployeeUpdate(PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'employee/employee_update_form.html'
    permission_required = 'change_post'


def search_employee(request):
    return render(request, 'employee/employee_search.html', locals())


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
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'shopping/order_step_1_create.html'
    success_url = reverse_lazy('product-list')

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            new_order = self.object
            request.session['new_order'] = new_order.order_id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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
            if request.POST.get('order'):
                order_detail = OrderDetail()
                order_detail.order = Order.objects.get(pk=request.POST.get('order'))
                inventory_id = request.POST.get('inventory')
                order_detail.inventory = Inventory.objects.get(pk=inventory_id)
                order_detail.quantity = request.POST.get('quantity')

                while inserted is False:
                    try:
                        order_detail.save()
                        Inventory.objects.filter(pk=inventory_id).update(quantity=F('quantity') - order_detail.quantity)
                        inserted = True
                    except IntegrityError:
                        query = OrderDetail.objects.filter(inventory=order_detail.inventory, order=order_detail.order)
                        query.update(quantity=F('quantity') + order_detail.quantity)
                        Inventory.objects.filter(pk=inventory_id).update(quantity=F('quantity') - order_detail.quantity)

                        break
                return redirect('order-summary')
        return redirect('product-list')


def save_invoice(order):
    date = datetime.date.today()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")

    base_number_str = year + month + day + str(order.cust.cust_id)
    serial_number_base = int(base_number_str)

    if Invoice.objects.filter(invoice_num__startswith=serial_number_base):
        queryset = Invoice.objects.filter(invoice_num__startswith=serial_number_base).first()
        serial_number = queryset.invoice_num + 1
        invoice = Invoice(order_id=order.order_id, pay_type=order.pay_type, emp=order.emp,
                          invoice_num=serial_number, total_price=order.total_price, status='Paid',
                          grand_total=order.grand_total, tax=order.tax, cust=order.cust)
        invoice.save()
    else:
        serial_number = int(base_number_str + '01')
        invoice = Invoice(order_id=order.order_id, pay_type=order.pay_type, emp=order.emp,
                          invoice_num=serial_number, total_price=order.total_price, status='Paid',
                          grand_total=order.grand_total, tax=order.tax, cust=order.cust)
        invoice.save()
    return invoice


class OrderSummaryView(generic.ListView):
    model = OrderDetail
    form_class = OrderDetailForm
    template_name = 'shopping/order_step_3_summary.html'

    def get_queryset(self):
        order_id = self.request.session['new_order']
        order = Order.objects.get(pk=order_id)
        return OrderDetail.objects.filter(order=order)

    def get_context_data(self, **kwargs):
        context = super(OrderSummaryView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        subtotal = 0
        for item in queryset:
            db_price = item.inventory.inv_price
            unit_price = Decimal(sub(r'[^\d.]', '', db_price))
            subtotal += unit_price*item.quantity

        subtotal = Money(subtotal, Currency.USD)
        tax = subtotal * SALES_TAX_RATE

        grand_total = subtotal + tax
        subtotal = subtotal.format('en_US')
        tax = tax.format('en_US')
        grand_total = grand_total.format('en_US')

        context['total'] = subtotal
        context['tax'] = tax
        context['grand_total'] = grand_total
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('detail_id'):
            detail_id = request.POST.get('detail_id')
            OrderDetail.objects.filter(detail_id=detail_id).delete()
            Inventory.objects.filter(
                pk=request.POST.get('inventory')).update(quantity=F('quantity') + request.POST.get('quantity'))
            return redirect('order-summary')

        if request.POST.get('submit_payment'):
            if request.POST.get('payment'):
                payment = request.POST.get('payment')
                total_price = request.POST.get('total')
                tax = request.POST.get('tax')
                grand_total = request.POST.get('grand_total')

                order_id = self.request.session['new_order']
                order = Order.objects.get(pk=order_id)
                order.pay_type = payment
                order.total_price = Decimal(sub(r'[^\d.]', '', total_price))
                order.tax = Decimal(sub(r'[^\d.]', '', tax))
                order.grand_total = Decimal(sub(r'[^\d.]', '', grand_total))
                order.status = 'Complete'
                order.save()

                invoice = save_invoice(order)
                request.session['invoice_id'] = invoice.invoice_id
                request.session['invoice_num'] = invoice.invoice_num
                return render(request, 'shopping/order_step_4_finish.html', )
            else:
                messages.error(request, 'Payment method is required.')
                return redirect('order-summary')

        elif request.POST.get('skip'):
            total_price = request.POST.get('total')
            tax = request.POST.get('tax')
            grand_total = request.POST.get('grand_total')

            order_id = self.request.session['new_order']
            order = Order.objects.get(pk=order_id)
            order.total_price = Decimal(sub(r'[^\d.]', '', total_price))
            order.tax = Decimal(sub(r'[^\d.]', '', tax))
            order.grand_total = Decimal(sub(r'[^\d.]', '', grand_total))
            order.status = 'Pending'
            order.save()
            return render(request, 'shopping/order_step_4_stored.html', )
        return redirect('order-summary')


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'
    paginate_by = 25


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order_details = OrderDetail.objects.filter(order_id=self.kwargs['pk'])
        context['order_details'] = order_details
        return context


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'order/order_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        order_details = OrderDetail.objects.filter(order_id=self.kwargs['pk'])
        context['order_details'] = order_details
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object(*args)

        if request.POST.get('pay_type'):
            emp = Employee.objects.get(pk=request.POST.get('emp'))
            order.emp = emp
            order.pay_type = request.POST.get('pay_type')
            order.status = 'Complete'
            order.save()

            invoice = save_invoice(order)
            request.session['invoice_id'] = invoice.invoice_id
            request.session['invoice_num'] = invoice.invoice_num
            return render(request, 'shopping/order_step_4_finish.html', )

        else:
            if request.POST.get('emp'):
                emp = Employee.objects.get(pk=request.POST.get('emp'))
                order.emp = emp
                order.save()
                return redirect('order-detail', pk=order.pk)


class OrderCancel(generic.DetailView):
    model = Order
    template_name = 'order/order_confirm_cancel.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCancel, self).get_context_data(**kwargs)
        order_details = OrderDetail.objects.filter(order_id=self.kwargs['pk'])
        context['order_details'] = order_details
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            Order.objects.filter(pk=self.kwargs['pk']).update(status='Cancelled')

            order_details = OrderDetail.objects.filter(order_id=self.kwargs['pk'])
            for item in order_details:
                Inventory.objects.filter(pk=item.inventory.pk).update(quantity=F('quantity') + item.quantity)

            return redirect('order-list')


class InvoiceListView(generic.ListView):
    model = Invoice
    queryset = Invoice.objects.all()
    template_name = 'invoice/invoice_list.html'
    paginate_by = 25


# TODO: invoice print
class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'invoice/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.kwargs['pk'])
        order_details = OrderDetail.objects.filter(order_id=invoice.order)
        context['order_details'] = order_details
        return context


class InvoiceDelete(DeleteView):
    model = Invoice
    template_name = 'invoice/invoice_confirm_delete.html'
    success_url = reverse_lazy('invoice-list')


