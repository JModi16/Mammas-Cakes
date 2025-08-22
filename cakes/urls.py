from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page URLs
    path('', views.home, name='home'),
    path('vegan-cakes/', views.vegan_cakes, name='vegan_cakes'),
    path('birthday-cakes/', views.birthday_cakes, name='birthday_cakes'),
    path('wedding-cakes/', views.wedding_cakes, name='wedding_cakes'),
    path('treats/', views.treats, name='treats'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),

    # Authentication URLs
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
         name='logout'),

    # Password Reset URLs
    path('accounts/password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('accounts/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Order URLs (replace cart URLs)
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<str:order_number>/',
         views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<str:order_number>/', views.order_detail,
         name='order_detail'),
    path('orders/<str:order_number>/confirmation/',
         views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
]