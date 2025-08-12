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
from .models import Order, OrderItem, Customer
from .forms import CustomUserCreationForm

logger = logging.getLogger(__name__)

# Existing views
def home(request):
    return render(request, 'cakes/home.html')

def birthday_cakes(request):
    return render(request, 'cakes/birthday_cakes.html')

def wedding_cake(request):
    return render(request, 'cakes/wedding_cakes.html')

def vegan_cakes(request):
    return render(request, 'cakes/vegan_cakes.html')

def treats(request):
    return render(request, 'cakes/treats.html')

def products(request):
    query = request.GET.get('q', '')
    context = {'query': query}
    return render(request, 'cakes/products.html', context)

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            Customer.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number', '')
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Order processing
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def process_order(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['customer', 'orderType', 'items', 'subtotal', 'total']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'success': False, 'error': f'Missing required field: {field}'})
        
        # Create order
        order = Order.objects.create(
            customer=request.user,
            order_type=data['orderType'],
            customer_name=data['customer']['name'],
            customer_email=data['customer']['email'],
            customer_phone=data['customer']['phone'],
            special_instructions=data.get('specialInstructions', ''),
            subtotal=Decimal(str(data['subtotal'])),
            delivery_fee=Decimal(str(data.get('deliveryFee', 0))),
            total=Decimal(str(data['total']))
        )
        
        # Add collection/delivery details
        if data['orderType'] == 'collection':
            order.collection_date = datetime.strptime(data['collection']['date'], '%Y-%m-%d').date()
            order.collection_time = data['collection']['time']
        else:
            order.delivery_address = data['delivery']['address']
            order.delivery_city = data['delivery']['city']
            order.delivery_postcode = data['delivery']['postcode']
            order.delivery_date = datetime.strptime(data['delivery']['date'], '%Y-%m-%d').date()
            order.delivery_time = data['delivery'].get('time', '')
        
        order.save()
        
        # Create order items
        for item in data['items']:
            OrderItem.objects.create(
                order=order,
                cake_id=item['id'],
                cake_name=item['name'],
                cake_image=item['image'],
                unit_price=Decimal(str(item['price'])),
                quantity=item['quantity']
            )
        
        # Send confirmation email
        send_order_confirmation_email(order)
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'message': 'Order placed successfully!'
        })
        
    except Exception as e:
        logger.error(f"Order processing error: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to process order'})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('items')
    return render(request, 'cakes/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    return render(request, 'cakes/order_detail.html', {'order': order})

def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - {order.order_number}'
        
        # Render email template
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'items': order.items.all()
        })
        
        plain_message = render_to_string('emails/order_confirmation.txt', {
            'order': order,
            'items': order.items.all()
        })
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Order confirmation email sent for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email for order {order.order_number}: {str(e)}")