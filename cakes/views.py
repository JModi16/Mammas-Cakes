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
import uuid

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
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Generate unique order number
        order_number = f"MC{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        
        # Get or create customer profile
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'phone_number': data.get('customer_phone', ''),
                'address': data.get('delivery_address', ''),
                'city': data.get('delivery_city', ''),
                'postcode': data.get('delivery_postcode', ''),
            }
        )
        
        # Update customer info if changed
        if not created:
            customer.phone_number = data.get('customer_phone', customer.phone_number)
            if data.get('delivery_address'):
                customer.address = data.get('delivery_address')
                customer.city = data.get('delivery_city')
                customer.postcode = data.get('delivery_postcode')
            customer.save()
        
        # Get the cake
        try:
            cake = Cake.objects.get(id=data['cake_id'])
        except Cake.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Cake not found'
            })
        
        # Calculate total
        subtotal = Decimal(str(data['cake_price']))
        delivery_fee = Decimal('5.00') if data['delivery_option'] == 'delivery' else Decimal('0.00')
        total = subtotal + delivery_fee
        
        # Determine delivery date
        delivery_date = None
        if data['delivery_option'] == 'collection' and data.get('collection_date'):
            delivery_date = datetime.strptime(data['collection_date'], '%Y-%m-%d').date()
        elif data['delivery_option'] == 'delivery' and data.get('delivery_date'):
            delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%d').date()
        
        # Create the order
        order = Order.objects.create(
            customer=request.user,
            order_number=order_number,
            customer_email=data['customer_email'],
            total=total,
            status='pending',
            order_type='single_item',
            special_instructions=data.get('special_instructions', ''),
            delivery_date=delivery_date
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            cake=cake,
            cake_name=cake.name,
            cake_price=cake.price,
            quantity=1,
            total_price=subtotal
        )
        
        # Send confirmation email (optional)
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = f'Order Confirmation - {order_number}'
            message = f"""
            Dear {data['customer_name']},
            
            Thank you for your order!
            
            Order Number: {order_number}
            Cake: {cake.name}
            Total: £{total}
            
            We'll be in touch soon with updates.
            
            Best regards,
            Mamma's Cakes Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [data['customer_email']],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'success': True,
            'order_number': order_number,
            'message': f'Order placed successfully! Order number: {order_number}',
            'redirect_url': f'/order-confirmation/{order_number}/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        })
    except Exception as e:
        print(f"Order processing error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to process order. Please try again.'
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