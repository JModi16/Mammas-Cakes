from django.urls import path
from . import views

urlpatterns = [
    path('birthday-cakes/', views.birthday_cakes, name='birthday_cakes'),
    path('wedding-cakes/', views.wedding_cakes, name='wedding_cake'),
    path('treats/', views.treats, name='treats'),
    path('vegan-cakes/', views.vegan_cakes, name='vegan_cakes'),
    path('all-cakes-treats/', views.all_cakes_treats, name='all_cakes_treats'),
]