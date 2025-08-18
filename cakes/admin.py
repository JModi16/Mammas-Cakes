from django.contrib import admin
from .models import Cake, Customer, Order, OrderItem


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number',
        'customer',
        'total',
        'status',
        'created_at']
    list_filter = ['status', 'order_type', 'created_at']
    search_fields = ['order_number', 'customer__username', 'customer_email']
    readonly_fields = ['order_number', 'created_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'cake_name',
        'quantity',
        'cake_price',
        'total_price']
    list_filter = ['order__status']
