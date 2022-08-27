# from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
from slider.models import Slider
def home(request):
    products = Product.objects.all().filter(is_available = True)
    slider   = Slider.objects.all()
    print('slider',slider)
    
    context = {
        'products':products,
        'slider':slider,
    }
    return render(request,'home.html' ,context)