from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_date
import json
import logging
from decimal import Decimal
from datetime import datetime
import uuid
import random
import string
from .models import Cake, Order, OrderItem, Customer
from .forms import CustomUserCreationForm
from django.db import models

logger = logging.getLogger(__name__)

def generate_order_number():
    """Generate a unique order number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_chars = ''.join(random.choices(string.digits, k=4))
    return f"MC{timestamp}{random_chars}"

# Existing page views
def home(request):
    return render(request, 'cakes/home.html')

def birthday_cakes(request):
    """Display birthday cakes from database"""
    cakes = Cake.objects.filter(category='birthday', is_available=True)
    return render(request, 'cakes/birthday_cakes.html', {'cakes': cakes})

def wedding_cakes(request):
    """Display wedding cakes from database"""
    cakes = Cake.objects.filter(category='wedding', is_available=True)
    return render(request, 'cakes/wedding_cakes.html', {'cakes': cakes})

def vegan_cakes(request):
    """Display vegan cakes from database"""
    cakes = Cake.objects.filter(category='vegan', is_available=True)
    return render(request, 'cakes/vegan_cakes.html', {'cakes': cakes})

def treats(request):
    """Display treats from database"""
    cakes = Cake.objects.filter(category='treats', is_available=True)
    return render(request, 'cakes/treats.html', {'cakes': cakes})

def products(request):
    """Display all products"""
    cakes = Cake.objects.filter(is_available=True)
    return render(request, 'cakes/products.html', {'cakes': cakes})

# Authentication views
def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Order processing views
@csrf_exempt
@require_http_methods(["POST"])
def place_order(request):
    print(f"🔧 place_order view called - Method: {request.method}")
    print(f"🔧 User authenticated: {request.user.is_authenticated}")
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        print(f"🔧 Parsed data: {data}")
        
        # Validate required fields
        required_fields = ['cake_id', 'cake_name', 'cake_price', 'customer_name', 'customer_email', 'customer_phone', 'delivery_option']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'Missing required field: {field}'}, status=400)
        
        # Create order
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            customer_email=data['customer_email'],
            order_number=generate_order_number(),
            order_type=data['delivery_option'],
            total=Decimal(str(data['cake_price'])),
            special_instructions=data.get('special_instructions', ''),
            
            # Collection fields
            collection_date=data.get('collection_date') or None,
            collection_time=data.get('collection_time', ''),
            
            # Delivery fields
            delivery_address=data.get('delivery_address', ''),
            delivery_city=data.get('delivery_city', ''),
            delivery_postcode=data.get('delivery_postcode', ''),
            delivery_date=data.get('delivery_date') or None,
            delivery_time=data.get('delivery_time', ''),
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            cake_name=data['cake_name'],
            quantity=1,
            price=Decimal(str(data['cake_price']))
        )
        
        # Send confirmation email
        try:
            send_order_confirmation_email(order)
            print(f"✅ Order confirmation email sent for {order.order_number}")
        except Exception as email_error:
            print(f"⚠️ Email sending failed: {email_error}")
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'message': 'Order placed successfully!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': 'Failed to create order'}, status=500)

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(customer=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'cakes/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    """Display detailed view of a specific order"""
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    return render(request, 'cakes/order_detail.html', {'order': order})

@login_required
def order_confirmation(request, order_number):
    try:
        order = Order.objects.get(
            order_number=order_number,
            customer=request.user
        )
        return render(request, 'cakes/order_confirmation.html', {
            'order': order
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('home')

def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - {order.order_number}'
        
        # Use the email template with delivery details
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'customer_name': order.customer.first_name or order.customer.username,
        })
        
        plain_message = f"""
        Dear {order.customer.first_name or order.customer.username},
        
        Thank you for your order!
        
        Order Number: {order.order_number}
        Total: £{order.total}
        
        We'll prepare your delicious cake with love and care.
        
        Best regards,
        Mammas Cakes Team
        """
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Confirmation email sent for order {order.order_number}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email for order {order.order_number}: {e}")
        raise