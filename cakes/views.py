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
from .models import Cake, Order, OrderItem, Customer
from .forms import CustomUserCreationForm
from django.db import models

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

@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            # Log raw request data
            raw_data = request.body.decode('utf-8')
            print(f"Raw request data: {raw_data}")
            
            data = json.loads(request.body)
            print(f"Parsed data: {data}")
            
            # Parse dates properly
            collection_date = None
            delivery_date = None
            
            if data.get('collection_date'):
                try:
                    collection_date = parse_date(data.get('collection_date'))
                    print(f"Parsed collection_date: {collection_date}")
                except Exception as e:
                    print(f"Error parsing collection_date: {e}")
                    collection_date = None
                    
            if data.get('delivery_date'):
                try:
                    delivery_date = parse_date(data.get('delivery_date'))
                    print(f"Parsed delivery_date: {delivery_date}")
                except Exception as e:
                    print(f"Error parsing delivery_date: {e}")
                    delivery_date = None
            
            # Create the order with error handling
            order_data = {
                'customer': request.user,
                'customer_email': data.get('customer_email'),
                'order_number': f"MC{timezone.now().strftime('%Y%m%d%H%M%S')}",
                'order_type': data.get('delivery_option', 'collection'),
                'special_instructions': data.get('special_instructions', ''),
            }
            
            # Add new fields only if they exist in the model
            try:
                order_data.update({
                    'collection_date': collection_date,
                    'collection_time': data.get('collection_time', ''),
                    'delivery_address': data.get('delivery_address', ''),
                    'delivery_city': data.get('delivery_city', ''),
                    'delivery_postcode': data.get('delivery_postcode', ''),
                    'delivery_date': delivery_date,
                    'delivery_time': data.get('delivery_time', ''),
                })
            except Exception as e:
                print(f"Warning: Some fields not available in model: {e}")
            
            order = Order.objects.create(**order_data)
            print(f"Order created: {order.order_number}")
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                cake_name=data.get('cake_name'),
                cake_price=Decimal(str(data.get('cake_price', 0))),
                quantity=1,
                total_price=Decimal(str(data.get('cake_price', 0)))
            )
            
            # Update order total
            order.total = order.items.aggregate(
                total=models.Sum('total_price')
            )['total'] or Decimal('0')
            order.save()
            print(f"Order total updated: £{order.total}")
            
            # Send confirmation email
            try:
                send_order_confirmation_email(order)
                print(f"✅ Email sent successfully to {order.customer_email}")
            except Exception as e:
                print(f"❌ Email error: {e}")
            
            return JsonResponse({
                'success': True, 
                'message': 'Order placed successfully!',
                'order_number': order.order_number
            })
            
        except Exception as e:
            print(f"❌ Order creation error: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

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