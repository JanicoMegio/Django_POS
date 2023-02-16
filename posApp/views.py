from dis import disco
from multiprocessing import context
from pickle import FALSE
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from numpy import product
from posApp.models import Category, Products, Sales, salesItems, Inventoryrecord
from django.db.models import Count, Sum, F, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
import json
import sys
import csv
import os
from datetime import date, datetime, timedelta


# Login


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)    
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# user profile
def restore(request):
    password = request.user.password
    context = {
        'page_title': 'Restore', 
        'password': password
    }
    return render(request, 'posApp/restore.html', context)

# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.

@login_required
def home(request):
    data = []
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    product_list = Products.objects.all()
    product_listed = Products.objects.all()
    sales = salesItems.objects.values('date').order_by('date').annotate(Sum('total'))
    sales_date = list(sales.values("date"))
    sales_value = list(sales.values("total__sum"))
    value = []
    key = []
    for i in sales_date:
        value.append(i["date"])
    for i in sales_value:
        key.append(i["total__sum"])

    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total', flat=True))

    context = {
        'page_title': 'Home',
        'categories': categories,
        'products': products, 
        'product_listed': product_listed,
        'product_list':product_list,
        'transaction': transaction,
        'total_sales': total_sales,
        'sales': sales,
        'value': value,
        'key': key,
        
    }
    return render(request, 'posApp/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'posApp/about.html', context)

#export csv record

@login_required
def record_csv(request):
    resp = {'status': 'failed'}
    current_date = datetime.now().date()
    try:
        if request.method == 'POST':
            response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': f'attachment; filename="Inventory_Report:{current_date}.csv"'})
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            category = request.POST.get('category-list')
            action = request.POST.get('inventoryaction')
            print(action)
            records = Inventoryrecord.objects.filter(Q(st_date__gte=fromdate, st_date__lte=todate) & Q(product_name__category_id__name__contains = category) & Q(status__contains = action))
            stock_record = Inventoryrecord.objects.filter(Q(st_date__gte=fromdate, st_date__lte=todate) & Q(product_name__category_id__name__contains = category) & Q(status__contains = action)).aggregate(Sum('amount_stock')).get('amount_stock__sum',0)
            total = Inventoryrecord.objects.filter(Q(st_date__gte=fromdate, st_date__lte=todate) & Q(product_name__category_id__name__contains = category) & Q(status__contains = action)).aggregate(Sum('total')).get('total__sum',0.00)
            total_record = ('%.2f'%total)
            writer = csv.writer(response)
            writer.writerow(['Product', 'Stock', 'Amount', 'Status', 'Date'])
            for record in records:
                writer.writerow([record.product_name, record.amount_stock, record.total, record.status, record.st_date])
            writer.writerow(['',f'Total: {stock_record}', f'Total: {total_record}', '', ''])
            return response
           
            resp['status'] = 'success'
            messages.success(request, 'Successfully saved.')
    except:
            messages.info(request, 'No Record Found.')

    return redirect('/inventory')



@login_required
def manage_record(request):
    product_list = Category.objects.values_list('name', flat=True).distinct()
    context = {
        'product_list': product_list,
    }
    return render(request, 'posApp/manage_report_csv.html', context)


@login_required
def inventory(request):
    product_list = Products.objects.all()
    context = {
        'page_title': 'Inventory',
        'products': product_list,
    
        
    }
    return render(request, 'posApp/inventory.html', context)

@login_required
def manage_inventory(request):
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'posApp/manage_inventory.html', context)

@login_required
def save_inventory(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_product = Products.objects.filter(id=data['id']).update(discount=int(data['discount']), status=data['status'])
        else:
            save_product = Products(discount=int(data['discount']), status=data['status'])
            save_product.save()
        resp['status'] = 'success'
        messages.success(request, 'Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def stock_in(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            stock_number = data['stocks']
            product_price = data['price']
            product = Products.objects.filter(id=data['id']).first()
            total = float(product_price) * float(stock_number)
            save_product = Products.objects.filter(id=data['id']).update(stocks=F('stocks') + stock_number)
            Inventoryrecord(product_name=product,amount_stock=data['stocks'],total=total, status='IN').save()
        else:
            save_product = Products(stocks=F('stocks') + stock_number)
            Inventoryrecord(product_name = product, amount_stock=data['stocks'], total=total, status='IN').save()
            save_product.save()
           
        resp['status'] = 'success'
        messages.success(request, 'Stock-in Successful')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def stock_manage_in(request):
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'posApp/stock_manage_in.html', context)

def stock_manage_out(request):
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'posApp/stock_manage_out.html', context)

def stock_out(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            stock_number = data['stocks']
            product_price = data['price']
            product = Products.objects.filter(id=data['id']).first()
            total = float(product_price) * float(stock_number)
            Products.objects.filter(id=data['id']).update(stocks=F('stocks') - stock_number)
            Inventoryrecord(product_name = product, amount_stock=data['stocks'], total=total, status='OUT').save()
        else:
            save_product = Products(stocks=F('stocks') - stock_number)
            Inventoryrecord(product_name = product, amount_stock=data['stocks'], total=total, status='OUT').save()
            save_product.save()
        resp['status'] = 'success'
        messages.success(request, 'Stock-out Successful.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title': 'Category List',
        'category': category_list,
    }
    return render(request, 'posApp/category.html', context)


@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()

    context = {
        'category': category
    }
    return render(request, 'posApp/manage_category.html', context)


@login_required
def save_category(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_category = Category.objects.filter(id=data['id']).update(
                name=data['name'],status=data['status'])
        else:
            save_category = Category(
                name=data['name'],status=data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_category(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Category.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products

@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title': 'Product List',
        'products': product_list,
    }
    return render(request, 'posApp/products.html', context)


@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'posApp/manage_product.html', context)


def test(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'posApp/test.html', context)


@login_required
def save_product(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0:
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id=data['category_id']).first()

        try:
            if (data['id']).isnumeric() and int(data['id']) > 0:
                save_product = Products.objects.filter(id=data['id']).update(code=data['code'], category_id=category, name=data['name'], description=data['description'], price=float(
                    data['price']))

            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description=data['description'], price=float(
                    data['price']))
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_product(request):
    data = request.POST
    resp = {'status': ''}
    chrt = 0
    try:
        Products.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def pos(request):
    products = Products.objects.filter(status=1)
    product_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'code': product.code, 'price': float(
            product.price), 'stock': int(product.stocks), 'discount': int(product.discount)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html', context)


@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
    }
    return render(request, 'posApp/checkout.html', context)


#save csv
@login_required
def save_csv(request):
    resp = {'status': 'failed'}
    current_date = datetime.now().date()
    try:
        if request.method == 'POST':
            response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': f'attachment; filename="Sales_Report:{current_date}.csv"'})
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            print(fromdate)
            category = request.POST.get('category-list')
            sales = salesItems.objects.filter(Q(date__gte=fromdate, date__lte=todate) & Q(product_id__category_id__name__contains = category))
            total = list(salesItems.objects.filter(Q(date__gte=fromdate, date__lte=todate) & Q(product_id__category_id__name__contains = category)).aggregate(Sum('total')).values())[0]
            writer = csv.writer(response)
            total_record = ('%.2f'%total)
            print(category)
            writer.writerow(['ID', 'Product', 'Items','Discount Amount', 'Total', 'Date'])
            for sale in sales:
                writer.writerow([sale.sale_id, sale.product_id, sale.qty,sale.price, sale.total, sale.date])
            writer.writerow(['','','','',f'TOTAL: {total_record}',''])
            
            return response
    except:
            messages.info(request, 'No Record Found.')
            #print(sales_sample)
    return redirect('/sales')


@login_required
def manage_csv(request):
    product_list = Category.objects.values_list('name', flat=True).distinct()
    context = {
        'product_list': product_list,
    }
    return render(request, 'posApp/manage_csv.html', context)


@login_required
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)
    try:
        sales = Sales(code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                      grand_total=data['grand_total'], tendered_amount=data['tendered_amount'], amount_change=data['amount_change']).save()
        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
                product_id = prod
                sale = Sales.objects.filter(id=sale_id).first()
                product = Products.objects.filter(id=product_id).first()
                qty = data.getlist('qty[]')[i]
                price = data.getlist('price[]')[i]
                stock = data.getlist('stocks[]')[i]
                discount = data.getlist('discount[]')[i]
                discount_get = float(discount) / 100
                total_discount = float(price) * float(discount_get)
                discounted_amount = float(price) - float(total_discount)
                updated_stock = int(stock) - int(qty)
                Products.objects.filter(id=product_id).update(stocks=updated_stock)
                Products.objects.filter(id=product_id).update(chart_stock=F('chart_stock') + qty)
                total = float(discounted_amount) * float(qty)
                print({'sale_id': sale, 'product_id': product,
                      'qty': qty, 'price': price, 'total': total})
                print(product)
                salesItems(sale_id=sale, product_id=product,
                           qty=qty, price=total_discount, total=total).save()
                i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Payment Successful.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def salesList(request):

    sales = Sales.objects.all()[0:50]
    sale_data = []
    if request.method == 'POST':
        search = request.POST['search']
        sales = Sales.objects.filter(code__contains=search)
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = salesItems.objects.filter(sale_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        sale_data.append(data)
    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
    }
        #return HttpResponse('')
    return render(request, 'posApp/sales.html', context)


@login_required
def showresult(request):
    if request.POST:
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        sales = Sales.objects.filter(date_added__gte=fromdate, date_added__lte=todate)

    return render(request, 'posApp/sales.html')

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id=sales).all()
    context = {
        "transaction": transaction,
        "salesItems": ItemList
    }

    return render(request, 'posApp/receipt.html', context)
    # return HttpResponse('')


@login_required
def delete_sale(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

@login_required
def restore_database(request):
    resp = {'status': 'failed', 'msg': ''}
    try:
        if request.method == 'POST':
            auth_pass = request.POST.get('password')
            u = User.objects.all().first()
            if check_password(auth_pass, u.password):
                os.system('cmd  /c "echo y | python manage.py dbrestore"')
                messages.info(request, 'User Authorized Database Restored.')
            else:
                messages.info(request, 'Unauthorized User.')
    except:
        messages.info(request, 'Authentication Failed.')
    return redirect('/restore')

