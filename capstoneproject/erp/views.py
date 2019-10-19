from django.shortcuts import render
from django.http import HttpResponse

from erp.models import Employee
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ERP index.")


def home(request):
    return render(request, 'home.html', )


def listall(request):

    employee = Employee.objects.all().order_by('emp_id')
    return render(request,'listall.html',locals())



