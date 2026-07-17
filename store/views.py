from django.shortcuts import render
from .models import Product
from category.models import Category
from django.shortcuts import get_object_or_404
# Create your views here.

def store(req,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
    else:    
        products=Product.objects.all().filter(is_available=True)
    context={
        'products':products
    }
    return render(req,"store/store.html",context)

def product_detail(req,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context={
        'single_product':single_product
    }    
    return render(req,"store/product_detail.html",context)
