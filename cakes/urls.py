from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('vegan-cakes/', views.vegan_cakes, name='vegan_cakes'),
    path('birthday-cakes/', views.birthday_cakes, name='birthday_cakes'),
    path('wedding-cakes/', views.wedding_cakes, name='wedding_cake'),
    path('treats/', views.treats, name='treats'),
    path('all-cakes-treats/', views.all_cakes_treats, name='all_cakes_treats'),
    path('products/', views.products, name='products'),

     # Authentication URLs
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]