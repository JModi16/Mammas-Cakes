from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page URLs
    path('', views.home, name='home'),
    path('vegan-cakes/', views.vegan_cakes, name='vegan_cakes'),
    path('birthday-cakes/', views.birthday_cakes, name='birthday_cakes'),
    path('wedding-cakes/', views.wedding_cakes, name='wedding_cakes'),  # Changed: Match your view function name
    path('treats/', views.treats, name='treats'),
    path('products/', views.products, name='products'),

    # Authentication URLs
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Order management URLs
    path('process-order/', views.process_order, name='process_order'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
]
