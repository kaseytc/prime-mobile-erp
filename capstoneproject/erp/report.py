from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from datetime import date
from django.db import connection
from django.db.models import Sum
from django.shortcuts import render
from django_pandas.io import read_frame
from bokeh.plotting import figure

from .models import Customer, Employee, Inventory, Invoice, Order, OrderDetail

import pandas as pd


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
    df['Age Group'] = pd.Categorical(df['Age Group'], ['< 20', '20-30', '30-40', '40-50', '50-60', '> 60'])
    df = df.sort_values(by=['Age Group', 'Unit Sold'], ascending=[True, False])
    df = df.drop(['Age', ], axis=1)

    return df


def get_age_group(age):
    df = get_customer_sales_data()
    df['Inventory'] = df['Make'] + " " + df['Model']
    df = df.drop(['Inventory ID', ], axis=1)

    if age is 0:
        return df[df['Age Group'] == '< 20']
    if age is 20:
        return df[df['Age Group'] == '20-30']
    if age is 30:
        return df[df['Age Group'] == '30-40']
    if age is 40:
        return df[df['Age Group'] == '40-50']
    if age is 50:
        return df[df['Age Group'] == '50-60']
    if age is 60:
        return df[df['Age Group'] == '> 60']


def customer_sales_table(request):
    df = get_customer_sales_data()

    source = ColumnDataSource(df)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]  # bokeh columns
    data_table = DataTable(columns=columns, source=source)
    script, div = components(data_table)
    return render(request, 'report/customer_sales_table.html', {'script': script, 'div': div, })


def get_plot(age):
    df = get_age_group(age)

    source = ColumnDataSource(df)
    inventory = source.data['Inventory'].tolist()
    unit_sold = source.data['Unit Sold'].tolist()
    title = "Unit Sold: Age " + df.iloc[0]["Age Group"]

    p = figure(x_range=inventory, plot_height=250, title=title,
               toolbar_location=None, tools="")
    p.vbar(x=inventory, top=unit_sold, width=0.6)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return p


def customer_sales_graph(request):
    components_dict = dict()

    try:
        p_0 = get_plot(0)
        script, div = components(p_0)
        components_dict.update({'script': script, 'div': div, })
    except IndexError:
        pass

    try:
        p_20 = get_plot(20)
        script2, div2 = components(p_20)
        components_dict.update({'script2': script2, 'div2': div2, })
    except IndexError:
        pass

    try:
        p_30 = get_plot(30)
        script3, div3 = components(p_30)
        components_dict.update({'script3': script3, 'div3': div3, })
    except IndexError:
        pass

    try:
        p_40 = get_plot(40)
        script4, div4 = components(p_40)
        components_dict.update({'script4': script4, 'div4': div4, })
    except IndexError:
        pass

    try:
        p_50 = get_plot(50)
        script5, div5 = components(p_50)
        components_dict.update({'script5': script5, 'div5': div5, })
    except IndexError:
        pass

    try:
        p_60 = get_plot(60)
        script6, div6 = components(p_60)
        components_dict.update({'script6': script6, 'div6': div6, })
    except IndexError:
        pass

    return render(request, 'report/customer_sales_graph.html', components_dict)











