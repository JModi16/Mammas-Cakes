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

# Comment out these imports until you create the models
# from .models import Order, OrderItem, Customer
from .forms import CustomUserCreationForm

logger = logging.getLogger(__name__)

# Existing page views
def home(request):
    return render(request, 'cakes/home.html')

def birthday_cakes(request):
    return render(request, 'cakes/birthday_cakes.html')

def wedding_cakes(request):
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
    """User registration view"""
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

# Comment out these functions until models are created:

# @login_required
# def order_history(request):
#     orders = Order.objects.filter(customer=request.user).prefetch_related('items')
#     return render(request, 'cakes/order_history.html', {'orders': orders})

# @login_required
# def order_detail(request, order_number):
#     order = get_object_or_404(Order, order_number=order_number, customer=request.user)
#     return render(request, 'cakes/order_detail.html', {'order': order})

# def send_order_confirmation_email(order):
#     """Send order confirmation email to customer"""
#     try:
#         subject = f'Order Confirmation - {order.order_number}'
        
#         # Render email template
#         html_message = render_to_string('emails/order_confirmation.html', {
#             'order': order,
#             'items': order.items.all()
#         })
        
#         plain_message = render_to_string('emails/order_confirmation.txt', {
#             'order': order,
#             'items': order.items.all()
#         })
        
#         send_mail(
#             subject=subject,
#             message=plain_message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[order.customer_email],
#             html_message=html_message,
#             fail_silently=False,
#         )
        
#         logger.info(f"Order confirmation email sent for order {order.order_number}")
        
#     except Exception as e:
#         logger.error(f"Failed to send confirmation email for order {order.order_number}: {str(e)}")

# Cart Management Views
def get_cart(request):
    """Get cart from session"""
    cart = request.session.get('cart', {})
    return cart

def get_cart_total(cart):
    """Calculate cart total"""
    total = 0
    for item in cart.values():
        total += Decimal(str(item['price'])) * item['quantity']
    return total

def get_cart_count(cart):
    """Get total items in cart"""
    return sum(item['quantity'] for item in cart.values())

def view_cart(request):
    """View shopping cart"""
    cart = get_cart(request)
    cart_items = []
    
    for cake_id, item in cart.items():
        cart_items.append({
            'cake_id': cake_id,
            'name': item['name'],
            'price': Decimal(str(item['price'])),
            'quantity': item['quantity'],
            'image': item['image'],
            'total': Decimal(str(item['price'])) * item['quantity']
        })
    
    context = {
        'cart_items': cart_items,
        'cart_total': get_cart_total(cart),
        'cart_count': get_cart_count(cart),
    }
    return render(request, 'cakes/cart.html', context)

@require_http_methods(["POST"])
def add_to_cart(request):
    """Add item to cart"""
    try:
        data = json.loads(request.body)
        cake_id = data.get('cake_id')
        cake_name = data.get('cake_name')
        cake_price = data.get('cake_price')
        cake_image = data.get('cake_image')
        quantity = int(data.get('quantity', 1))
        
        # Get cart from session
        cart = get_cart(request)
        
        # Add or update item in cart
        if cake_id in cart:
            cart[cake_id]['quantity'] += quantity
        else:
            cart[cake_id] = {
                'name': cake_name,
                'price': float(cake_price),
                'quantity': quantity,
                'image': cake_image
            }
        
        # Save cart to session
        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'{cake_name} added to cart!',
            'cart_count': get_cart_count(cart),
            'cart_total': float(get_cart_total(cart))
        })
        
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Error adding item to cart'
        })

@require_http_methods(["POST"])
def update_cart(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        cake_id = data.get('cake_id')
        quantity = int(data.get('quantity', 1))
        
        cart = get_cart(request)
        
        if cake_id in cart:
            if quantity > 0:
                cart[cake_id]['quantity'] = quantity
            else:
                del cart[cake_id]
            
            request.session['cart'] = cart
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'cart_count': get_cart_count(cart),
                'cart_total': float(get_cart_total(cart))
            })
        
        return JsonResponse({
            'success': False,
            'message': 'Item not found in cart'
        })
        
    except Exception as e:
        logger.error(f"Error updating cart: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Error updating cart'
        })

@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        cake_id = data.get('cake_id')
        
        cart = get_cart(request)
        
        if cake_id in cart:
            del cart[cake_id]
            request.session['cart'] = cart
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': get_cart_count(cart),
                'cart_total': float(get_cart_total(cart))
            })
        
        return JsonResponse({
            'success': False,
            'message': 'Item not found in cart'
        })
        
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Error removing item'
        })

def clear_cart(request):
    """Clear entire cart"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared successfully!')
    return redirect('view_cart')