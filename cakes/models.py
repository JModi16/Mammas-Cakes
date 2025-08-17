from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Cake(models.Model):
    """Cake products model"""
    CATEGORY_CHOICES = [
        ('birthday', 'Birthday Cakes'),
        ('wedding', 'Wedding Cakes'),
        ('vegan', 'Vegan Cakes'),
        ('treats', 'Treats'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='cakes/', blank=True, null=True)
    ingredients = models.TextField(blank=True)
    allergens = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - £{self.price}"
    
    class Meta:
        ordering = ['category', 'name']

class Customer(models.Model):
    """Extended user profile for additional customer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Collection/Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    ORDER_TYPE_CHOICES = [
        ('collection', 'Collection'),
        ('delivery', 'Delivery'),
    ]

    # Basic fields
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_email = models.EmailField()
    order_number = models.CharField(max_length=20, unique=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')  # ✅ ADDED
    total = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    
    # Collection fields
    collection_date = models.DateField(null=True, blank=True)
    collection_time = models.CharField(max_length=50, blank=True)
    
    # Delivery fields  
    delivery_address = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=100, blank=True)
    delivery_postcode = models.CharField(max_length=20, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        customer_name = self.customer.username if self.customer else self.customer_email
        return f"Order {self.order_number} - {customer_name}"

    def get_status_display_badge(self):
        """Return Bootstrap badge class for status"""
        status_badges = {
            'pending': 'badge-warning',
            'confirmed': 'badge-info',
            'preparing': 'badge-primary',
            'ready': 'badge-success',
            'completed': 'badge-dark',
            'cancelled': 'badge-danger',
        }
        return status_badges.get(self.status, 'badge-secondary')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, null=True, blank=True)
    cake_name = models.CharField(max_length=200)
    cake_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cake_name} x {self.quantity}"