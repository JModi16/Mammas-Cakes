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