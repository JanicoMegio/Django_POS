from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
admin.site.site_header = "SABON STATION ADMIN"
admin.site.site_title = "SABON STATION"
admin.site.index_header = "SABON STATION"

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    path('category', views.category, name="category-page"),
    path('manage_category', views.manage_category, name="manage_category-page"),
    path('save_category', views.save_category, name="save-category-page"),
    path('delete_category', views.delete_category, name="delete-category"),
    path('products', views.products, name="product-page"),
    path('manage_products', views.manage_products, name="manage_products-page"),
    path('test', views.test, name="test-page"),
    path('save_product', views.save_product, name="save-product-page"),
    path('delete_product', views.delete_product, name="delete-product"),
    path('pos', views.pos, name="pos-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos', views.save_pos, name="save-pos"),
    path('sales', views.salesList, name="sales-page"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('delete_sale', views.delete_sale, name="delete-sale"),
    path('restore', views.restore, name="restore"),
    path('showresult', views.showresult, name="show-result"),
    path('inventory', views.inventory, name="inventory-page"),
    path('manage_inventory', views.manage_inventory, name="manage_inventory-page"),
    path('save_inventory', views.save_inventory, name="save_inventory-page"),
    path('stock_in', views.stock_in, name="stock_in"),
    path('stock_manage_in', views.stock_manage_in, name="stock_manage_in"),
    path('stock_out', views.stock_out, name="stock-out"),
    path('stock_manage_out', views.stock_manage_out, name="stock_manage_out"),
    path('save_csv', views.save_csv, name="save_csv"),
    path('manage_csv', views.manage_csv, name="manage_csv"),
    path('record_csv', views.record_csv, name="record_csv"),
    path('manage_record', views.manage_record, name="manage_record"),
    path('restore_database', views.restore_database, name="restore_database")

    #---
    #path('employees', views.employees, name="employee-page"),
    #path('manage_employees', views.manage_employees, name="manage_employees-page"),
    #path('save_employee', views.save_employee, name="save-employee-page"),
    #path('delete_employee', views.delete_employee, name="delete-employee"),
    #path('view_employee', views.view_employee, name="view-employee-page"),
]
