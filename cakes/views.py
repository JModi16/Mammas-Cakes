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
import json
import logging
from decimal import Decimal
from datetime import datetime

from .models import Cake, Customer, Order, OrderItem
from .forms import CustomUserCreationForm

logger = logging.getLogger(__name__)

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
            # Comment out until Customer model is created
            # Customer.objects.create(
            #     user=user,
            #     phone_number=form.cleaned_data.get('phone_number', '')
            # )
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
def process_order(request):
    """Process order from cart.js"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Please log in'})
    
    try:
        data = json.loads(request.body)
        
        # Generate order number
        order_number = f"MC{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Log the order (you can save to database later)
        logger.info(f"Order received: {order_number} for {data['customer']['email']}")
        
        return JsonResponse({
            'success': True,
            'order_number': order_number,
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        logger.error(f"Order processing error: {e}")
        return JsonResponse({'success': False, 'error': 'Order failed'})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def place_order(request):
    """Place immediate order for single item"""
    try:
        data = json.loads(request.body)
        
        # Generate order number
        order_number = f"MC{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create order in database
        order = Order.objects.create(
            order_number=order_number,
            customer=request.user,
            customer_email=request.user.email,
            total=Decimal(str(data['price'])),
            status='pending',
            order_type='single_item'
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            cake_name=data['name'],
            cake_price=Decimal(str(data['price'])),
            quantity=1,
            total_price=Decimal(str(data['price']))
        )
        
        # Send confirmation email (optional)
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            logger.warning(f"Failed to send confirmation email: {e}")
        
        logger.info(f"Order placed: {order_number} for {request.user.email}")
        
        return JsonResponse({
            'success': True,
            'order_number': order_number,
            'message': f'Order {order_number} placed successfully!',
            'redirect_url': f'/orders/{order_number}/'
        })
        
    except Exception as e:
        logger.error(f"Order placement error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to place order. Please try again.'
        })

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
    """Display order confirmation page"""
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    return render(request, 'cakes/order_confirmation.html', {'order': order})

def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - {order.order_number}'
        html_message = render_to_string('cakes/email/order_confirmation.html', {
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