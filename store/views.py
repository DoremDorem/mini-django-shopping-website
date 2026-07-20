from django.shortcuts import render,redirect
from .models import Product
from category.models import Category
from django.shortcuts import get_object_or_404
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
# Create your views here.

# def store(req,category_slug=None):
#     categories=None
#     products=None
#     if category_slug !=None:
#         categories=get_object_or_404(Category,slug=category_slug)
#         products=Product.objects.filter(category=categories,is_available=True)
#         paginator=Paginator(products,3)
#         page=req.GET.get('page')
#         paged_products=paginator.get_page(page)
#     else:    
#         products=Product.objects.all().filter(is_available=True).order_by('id')
#         paginator=Paginator(products,4)
#         page=req.GET.get('page')
#         paged_products=paginator.get_page(page)
#     #filter by price    
#     min_price = req.GET.get('min_price')
#     max_price = req.GET.get('max_price')
#     if min_price:
#         products = products.filter(price__gte=min_price)

#     if max_price:
#         products = products.filter(price__lte=max_price)

#     context = {
#         'products': products,
#     }
#     context={
#         'products':paged_products
#     }
#     return render(req,"store/store.html",context)




def store(req, category_slug=None):
    products=None
    categories = None

    if category_slug is not None:

        categories = get_object_or_404(
            Category,
            slug=category_slug
        )

        products = Product.objects.filter(
            category=categories,
            is_available=True
        )

    else:

        products = Product.objects.filter(
            is_available=True
        ).order_by('id')


    # Filter by price
    min_price = req.GET.get('min_price')
    max_price = req.GET.get('max_price')


    if min_price:

        products = products.filter(
            price__gte=min_price
        )


    if max_price:

        products = products.filter(
            price__lte=max_price
        )


    # Pagination filter ke baad hoga
    paginator = Paginator(products, 4)

    page = req.GET.get('page')

    paged_products = paginator.get_page(page)


    context = {
        'products': paged_products,
        'min_price': min_price,
        'max_price': max_price,
    }


    return render(
        req,
        "store/store.html",
        context
    )



def product_detail(req,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(req),product=single_product).exists()
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'in_cart':in_cart
    }    
    return render(req,"store/product_detail.html",context)


def serach(req):
    if "keyword" in req.GET:
        keyword=req.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
        else:
            return redirect('pageNotFound')   
    context={
        'products':products
    }        
    return render(req,'store/store.html',context)



