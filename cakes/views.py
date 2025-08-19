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
from .forms import CustomUserCreationForm, ContactForm
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
            messages.success(
                request,
                f'Account created for {username}! You can now log in.'
            )
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

        # Parse dates properly
        collection_date = None
        if data.get('collection_date'):
            collection_date = parse_date(data['collection_date'])
            print(f"🔧 Parsed collection_date: {collection_date}")

        delivery_date = None
        if data.get('delivery_date'):
            delivery_date = parse_date(data['delivery_date'])
            print(f"🔧 Parsed delivery_date: {delivery_date}")

        # Create order with parsed dates
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            customer_email=data['customer_email'],
            order_number=generate_order_number(),
            order_type=data['delivery_option'],
            total=Decimal(str(data['cake_price'])),
            special_instructions=data.get('special_instructions', ''),

            # Collection fields with parsed date
            collection_date=collection_date,
            collection_time=data.get('collection_time', ''),

            # Delivery fields with parsed date
            delivery_address=data.get('delivery_address', ''),
            delivery_city=data.get('delivery_city', ''),
            delivery_postcode=data.get('delivery_postcode', ''),
            delivery_date=delivery_date,
            delivery_time=data.get('delivery_time', ''),
        )

        # Create order item
        OrderItem.objects.create(
            order=order,
            cake_name=data['cake_name'],
            cake_price=Decimal(str(data['cake_price'])),
            quantity=1,
            total_price=Decimal(str(data['cake_price'])),
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
        return JsonResponse(
            {'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse(
            {'success': False, 'error': 'Failed to create order'}, status=500)


@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(
        customer=request.user
    ).prefetch_related(
        'items'
    ).order_by('-created_at')
    return render(request, 'cakes/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    """Display detailed view of a specific order"""
    order = get_object_or_404(
        Order,
        order_number=order_number,
        customer=request.user)
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


def contact(request):
    """Display contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'Not provided')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            event_date = form.cleaned_data.get('event_date', 'Not specified')

            # Create email content
            subject_display = dict(form.SUBJECT_CHOICES)[subject]
            email_subject = f"Contact Form: {subject_display}"
            email_message = f"""
New contact form submission from Mamma's Cakes website:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject_display}
Event Date: {event_date}

Message:
{message}

---
This message was sent from the Mamma's Cakes contact form.
            """

            try:
                # Send email to business
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=email,
                    recipient_list=['info@mammascakes.com'],
                    fail_silently=False,
                )

                # Send confirmation email to customer
                confirmation_subject = (
                    "Thank you for contacting Mamma's Cakes!"
                )
                confirmation_message = f"""
Dear {name},

Thank you for contacting Mamma's Cakes!
We have received your message regarding: {subject_display}

We will get back to you within 24 hours at {email}.

In the meantime, feel free to check out 
our delicious cake collections on our website.

Best regards,
The Mamma's Cakes Team

Phone: 07920554000
Email: info@mammascakes.com
Address: Moore Court, Howard Road, Edgware, HA7 1FA
                """

                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_message,
                    from_email='info@mammascakes.com',
                    recipient_list=[email],
                    fail_silently=True,
                )

                messages.success(
                    request,
                    'Thank you! Your message has been sent successfully. '
                    'We will get back to you within 24 hours.'
                )
                form = ContactForm()  # Reset form after successful submission

            except Exception as e:
                print(f"Error sending contact email: {e}")
                error_message = (
                    'Sorry, there was an error sending your message. '
                    'Please try again or call us directly at 07920554000.'
                )
                messages.error(request, error_message)
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Contact Us',
        'page_description': 'Get in touch for custom orders and inquiries'
    }

    return render(request, 'cakes/contact.html', context)


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'Order Confirmation - {order.order_number}'

        # Use the email template with delivery details
        html_message = render_to_string(
            'emails/order_confirmation.html',
            {
                'order': order,
                'customer_name': (
                    order.customer.first_name or
                    order.customer.username
                ),
            })

        customer_name = (
            order.customer.first_name or
            order.customer.username
        )
        plain_message = f"""
        Dear {customer_name},

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
        error_msg = (
            f"Failed to send confirmation email for order "
            f"{order.order_number}: {e}"
        )
        logger.error(error_msg)
        raise
