from django.db import models
from django.contrib.auth.models import User

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
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Collection'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('single_item', 'Single Item'),
        ('multiple_items', 'Multiple Items'),
        ('custom', 'Custom Order'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='single_item')
    special_instructions = models.TextField(blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Collection fields
    collection_date = models.DateField(blank=True, null=True)
    collection_time = models.CharField(max_length=20, blank=True)
    
    # Delivery fields
    delivery_address = models.TextField(blank=True)
    delivery_city = models.CharField(max_length=100, blank=True)
    delivery_postcode = models.CharField(max_length=20, blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, null=True, blank=True)
    cake_name = models.CharField(max_length=200)
    cake_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cake_name} x {self.quantity}"