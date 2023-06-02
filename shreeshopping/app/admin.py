from django.contrib import admin
from .models import Customer, Product,Cart,OrderPlace
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user', 
        'name', 
        'locality', 
        'city', 
        'zipcode', 
        'state']
admin.site.register(Customer,CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'selling_price',
        'discounted_price',
        'description',
        'brand',
        'category',
        'Product_image']
admin.site.register(Product,ProductAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'product',
        'quantity']

@admin.register(OrderPlace)
class OrderPlaceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'customer',
        'product',
        'quantity',
        'order_date',
        'status']