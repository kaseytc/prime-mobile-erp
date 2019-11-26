from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from datetime import date
from django.db import connection
from django.db.models import Sum
from django.shortcuts import redirect, render, render_to_response
from django_pandas.io import read_frame
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import HoverTool
from bokeh.io import output_file, show
from bokeh.transform import factor_cmap
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.palettes import Spectral5
import bokeh.palettes
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi

from .models import Customer, Employee, Inventory, Invoice, Order, OrderDetail

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def index(request):
    return render(request, 'report/report.html',locals())


def popular_phone(request):
    inventory = Inventory.objects.all()
    result = OrderDetail.objects.values('inventory').annotate(Sum('quantity'))
    df_i = read_frame(inventory, fieldnames=['inventory_id', 'sku', 'make', 'model'])
    df_od = pd.DataFrame(result)
    df_od = df_od.rename(columns={'inventory': 'inventory_id'})

    df_merge = pd.merge(df_i, df_od, on='inventory_id', how='right')
    df = df_merge.sort_values(by='quantity__sum', ascending=False)

    df = df.rename(columns={'inventory_id': 'Inventory ID', 'sku': 'SKU','make': 'Make',
                            'model': 'Model','quantity__sum': 'Unit Sold'})

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source )
    script, div = components(data_table)

    return render(request, 'report/popular_phone.html', {'script': script, 'div': div, })


def inventory_profits(request):
    query_invoice = str(Invoice.objects.values('order_id').query)
    df_invoice = pd.read_sql_query(query_invoice, connection)

    query_od = str(OrderDetail.objects.values('order_id', 'inventory_id', 'quantity').query)
    df_od = pd.read_sql_query(query_od, connection)

    query_inventory = str(Inventory.objects.values('inventory_id', 'make', 'model', 'inv_price', 'inv_cost').query)
    df_inventory = pd.read_sql_query(query_inventory, connection)

    df_merge_od_invoice = pd.merge(df_od, df_invoice, on='order_id', how='right')
    df_merge = pd.merge(df_inventory, df_merge_od_invoice, on='inventory_id', how='right')
    df_merge = df_merge.drop(['order_id', 'inventory_id'], axis=1)
    df_merge = df_merge.groupby(['make', 'model', 'inv_price', 'inv_cost', ], as_index=False).sum()
    df_merge['inv_price'] = df_merge['inv_price'].replace('[\$,]', '', regex=True).astype(float)
    df_merge['inv_cost'] = df_merge['inv_cost'].replace('[\$,]', '', regex=True).astype(float)
    df_merge['Profit'] = (df_merge['inv_price'] - df_merge['inv_cost']) * df_merge['quantity']
    df_merge = df_merge.sort_values(by='Profit', ascending=False)
    df_merge['Profit'] = ['${:,.2f}'.format(x) for x in df_merge['Profit']]

    df = df_merge.drop(['inv_price', 'inv_cost', 'quantity'], axis=1)
    df = df.rename(columns={'make': 'Make', 'model': 'Model'})

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source)
    script, div = components(data_table)
    return render(request, 'report/inventory_profits.html', {'script': script, 'div': div, })


def employee_sales(request):
    query_i = str(Invoice.objects.values('emp_id', 'total_price').query)
    df_i = pd.read_sql_query(query_i, connection)

    query_e = str(Employee.objects.values('emp_id', 'fname', 'lname').query)
    df_e = pd.read_sql_query(query_e, connection)

    df_merge = pd.merge(df_e, df_i, on='emp_id', how='right')
    df_merge['total_price'] = df_merge['total_price'].replace('[\$,]', '', regex=True).astype(float)

    df_merge = df_merge.groupby(['emp_id', 'fname', 'lname', ], as_index=False).sum()

    df = df_merge.sort_values(by='total_price', ascending=False)
    df['total_price'] = ['${:,.2f}'.format(x) for x in df['total_price']]
    df = df.rename(columns={'emp_id': 'Employee ID', 'fname': 'First Name', 'lname': 'Last Name',
                            'total_price': 'Total Sales',})

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source)
    script, div = components(data_table)
    return render(request, 'report/employee_sales.html', {'script': script, 'div': div, })


def get_customer_sales_data():
    query_o = str(Order.objects.values('order_id', 'cust_id').query)
    df_o = pd.read_sql_query(query_o, connection)

    query_od = str(OrderDetail.objects.values('order_id', 'inventory_id', 'quantity').query)
    df_od = pd.read_sql_query(query_od, connection)

    query_i = str(Inventory.objects.values('inventory_id', 'make', 'model').query)
    df_i = pd.read_sql_query(query_i, connection)

    query_c = str(Customer.objects.values('cust_id', 'dob', ).query)
    df_c = pd.read_sql_query(query_c, connection)

    # calculate actual age
    today = date.today()

    for i in df_c['dob'].iteritems():
        try:
            age = today.year - i[1].year - ((today.month, today.day) < (i[1].month, i[1].day))
            df_c.at[i[0], 'age'] = age
        except AttributeError:
            pass

    df_merge_od_i = pd.merge(df_i, df_od, on='inventory_id', how='right')
    df_merge_od_i_o = pd.merge(df_o, df_merge_od_i, on='order_id', how='right')
    df_merge = pd.merge(df_c, df_merge_od_i_o, on='cust_id', how='right')
    df_merge = df_merge.drop(['dob', 'cust_id', 'order_id', ], axis=1)

    df = df_merge.rename(columns={'age': 'Age', 'inventory_id': 'Inventory ID',
                                  'make': 'Make', 'model': 'Model', 'quantity': 'Unit Sold', })

    for i in df['Age'].iteritems():
        if i[1] < 20:
            df.at[i[0], 'Age Group'] = '< 20'
        elif 20 <= i[1] < 30:
            df.at[i[0], 'Age Group'] = '20-30'
        elif 30 <= i[1] < 40:
            df.at[i[0], 'Age Group'] = '30-40'
        elif 40 <= i[1] < 50:
            df.at[i[0], 'Age Group'] = '40-50'
        elif 50 <= i[1] < 60:
            df.at[i[0], 'Age Group'] = '50-60'
        else:
            df.at[i[0], 'Age Group'] = '> 60'

    df = df[['Age Group', 'Age', 'Inventory ID', 'Make', 'Model', 'Unit Sold']]
    df = df.groupby(['Age Group', 'Inventory ID', 'Make', 'Model'], as_index=False).sum()
    df = df.sort_values(by=['Age Group', 'Unit Sold'], ascending=[True, False])
    df = df.drop(['Age', ], axis=1)

    return df


def customer_sales_table(request):
    df = get_customer_sales_data()

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source)
    script, div = components(data_table)
    return render(request, 'report/customer_sales_table.html', {'script': script, 'div': div, })


