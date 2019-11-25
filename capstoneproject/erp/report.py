from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from django.db import connection
from django.db.models import Sum
from django.db.models import Avg, Count, Min, Sum
from django.shortcuts import redirect, render, render_to_response
from django_pandas.io import read_frame
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import HoverTool
from bokeh.io import output_file, show
from bokeh.transform import factor_cmap
from decimal import Decimal
from re import sub
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge

from .models import Customer, Employee, ErpUser, Inventory, Invoice, Order, OrderDetail

import datetime as DT
import io
import numpy as np
import pandas as pd
import datetime
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


'''
select date_part('year', AGE(c.dob)) as "age", od.inventory_id, i.make, i.model, count(date_part('year', AGE(c.dob)))
from public."Customer" as c 
join public."Order" as o
on o.cust_id = c.cust_id
join public."Order_Detail" as od
on o.order_id = od.order_id
join public."Inventory" as i
on od.inventory_id = i.inventory_id
group by(date_part('year', AGE(c.dob)), od.inventory_id, i.make, i.model)
order by count(date_part('year', AGE(c.dob))) desc


Sales per customer per age
'''
def customer_sales(request):
    query_o = str(Order.objects.values('order_id', 'cust_id').query)
    df_o = pd.read_sql_query(query_o, connection)

    query_od = str(OrderDetail.objects.values('order_id', 'inventory_id', 'quantity').query)
    df_od = pd.read_sql_query(query_od, connection)

    query_i = str(Inventory.objects.values('inventory_id', 'make', 'model').query)
    df_i = pd.read_sql_query(query_i, connection)

    query_c = str(Customer.objects.values('cust_id', 'dob',).query)
    df_c = pd.read_sql_query(query_c, connection)

    now = datetime.date.today().year
    df_c['year'] = pd.DatetimeIndex(df_c['dob']).year
    df_c['age'] = now - df_c['year']
    df_c = df_c.drop(['dob', ], axis=1)

    df_merge_od_i = pd.merge(df_i, df_od, on='inventory_id', how='right')
    df_merge_od_i_o = pd.merge(df_o, df_merge_od_i, on='order_id', how='right')
    df_merge_od_i_o_c = pd.merge(df_c, df_merge_od_i_o, on='cust_id', how='right')
    print(df_merge_od_i_o_c)

    # TODO: show bar chart or table
    df_merge = df_merge_od_i_o_c.groupby(['age', 'make', 'model', ], as_index=False).sum()
    series = df_merge_od_i_o_c.groupby(['age', 'make', 'model', ]).size()
    print(series.keys)
    print(type(series))
    df = df_merge
    #plt.clf()
    #df = series.plot(kind='bar')
    #plt.show()

    #source = ColumnDataSource(data=data)

    # get max possible value of plotted columns with some offset
    #p = figure(x_range=dates, y_range=(0, g1[['fail', 'Pass']].values.max() + 3),
    #           plot_height=250, title="Report",
    #           toolbar_location=None, tools="")

    #p.vbar(x=dodge('Report_datetime', -0.25, range=p.x_range), top='fail', width=0.4, source=source,
    #       color="#c9d9d3", legend=value("fail"))

   # p.vbar(x=dodge('Report_datetime', 0.25, range=p.x_range), top='Pass', width=0.4, source=source,
    #       color="#718dbf", legend=value("Pass"))

   # p.x_range.range_padding = 0.1
   # p.xgrid.grid_line_color = None
   # p.legend.location = "top_left"
   # p.legend.orientation = "horizontal"

    #df = pd.DataFrame(df_merge)

    #df = df_merge.sort_values(by='Profit', ascending=False)

    #df_merge_od_i_o = pd.merge(df_o, df_merge_od_i, on='order_id', how='right')
    #print(df_merge_od_i)
    #df_merge = pd.merge(df_inventory, df_merge_od_invoice, on='inventory_id', how='right')
    #df_merge = df_merge.drop(['order_id', 'inventory_id'], axis=1)
    #df_merge = df_merge.groupby(['make', 'model', 'inv_price', 'inv_cost', ], as_index=False).sum()
    #df_merge['inv_price'] = df_merge['inv_price'].replace('[\$,]', '', regex=True).astype(float)
    #df_merge['inv_cost'] = df_merge['inv_cost'].replace('[\$,]', '', regex=True).astype(float)
    #df_merge['Profit'] = (df_merge['inv_price'] - df_merge['inv_cost']) * df_merge['quantity']
    #df_merge['Profit'] = ['${:,.2f}'.format(x) for x in df_merge['Profit']]

    #df = df_merge.drop(['inv_price', 'inv_cost', 'quantity'], axis=1)
    #df = df.sort_values(by='Profit', ascending=False)
    #df = df.rename(columns={'make': 'Make', 'model': 'Model'})

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source)
    script, div = components(data_table)
    return render(request, 'report/customer_sales.html', {'script': script, 'div': div, })
    #return render(request, 'report/customer_sales.html',locals())













