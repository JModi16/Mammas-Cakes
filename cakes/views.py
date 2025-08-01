
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm

from django.shortcuts import render

def home(request):
    return render(request, 'cakes/home.html')

def vegan_cakes(request):
    return render(request, 'cakes/vegan_cakes.html')

def birthday_cakes(request):
    return render(request, 'cakes/birthday_cakes.html')

def wedding_cakes(request):
    return render(request, 'cakes/wedding_cakes.html')

def treats(request):
    return render(request, 'cakes/treats.html')

def all_cakes_treats(request):
    return render(request, 'cakes/all_cakes_treats.html')

def products(request):
    query = request.GET.get('q', '')
    return render(request, 'cakes/products.html', {'query': query})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Mammas Cakes!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'cakes/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'cakes/profile.html')