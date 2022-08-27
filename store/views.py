from contextlib import redirect_stderr
from itertools import product
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductGallery, ReviewRating
from category.models import Category
from orders.models import OrderProduct

from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger , Paginator
from django.db.models import Q 
from .forms import ReviewForm

from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
def store(request ,category_slug=None):
    categories = None
    products = None 
    if category_slug != None :
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories ,is_available = True)
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()
    
    context = {
        
        # 'products':products,
        'products':paged_products,
        'products_count':total_products,
    }
    return render(request, 'store/store.html' , context)

def product_detail(request,category_slug , product_slug ):
    try:
        single_product = Product.objects.get(category__slug = category_slug , slug = product_slug)
        
        cart_item = CartItem.objects.filter(cart__cart_id = _cart_id(request),product = single_product).exists() # if item is exist in cart it will return True otherwise return false 
        # return HttpResponse(cart_item)
        # exit()
        
    
    except Exception as e:
        raise e
    
    # to check this is purchased or not 
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user = request.user , product_id = single_product.id).exists()
            
        except OrderProduct.DoesNotExist:
            order_product = None 
    else:
        order_product = None
        
        
    # except order_product.DoesNotExist:
    #     order_product = None
        
        
    # get the review
    reviews = ReviewRating.objects.filter(product_id = single_product.id , status = True)
    
    
    
    # Get the product gallery 
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)
    
    context = {
        'single_product':single_product,
        'cart_item'      :cart_item,
        'product_gallery' :product_gallery,
        'order_product':order_product,
        'reviews':reviews
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains = keyword))
            total_products = products.count()
        else:
            products = None
            total_products = None
    context = {
        'products':products,
        'products_count':total_products,
    }
    return render(request, 'store/store.html',context)


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method=='post' or request.method== 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST , instance=reviews)
            form.save()
            messages.success(request,'Thank you ! Your review has been updated .')
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review  = form.cleaned_data['review']
                data.rating  = form.cleaned_data['rating']
                data.ip      = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id    = request.user.id
                data.save()
                messages.success(request,'Thank you ! Your review has been added.')
                return redirect(url)
            
def laptop_latest_product(request):
    categories = None
    products = None
    category_slug = 'laptop'
    if category_slug == 'laptop':
        if category_slug != None :
            categories = get_object_or_404(Category, slug = category_slug)
            products = Product.objects.filter(category = categories ,is_available = True).order_by('-created_date')
            paginator = Paginator(products,3)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()
        else:
            products = Product.objects.all().filter(is_available = True).order_by('-created_date')
            paginator = Paginator(products,8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()
        
        context = {
            
            # 'products':products,
            'products':paged_products,
            'products_count':total_products,
        }
        return render(request, 'store/store.html' , context)
    
def television_latest_product(request):
    categories = None
    products = None
    category_slug = 'television'
    if category_slug == 'television':
        if category_slug != None :
            print( category_slug)
            categories = get_object_or_404(Category, slug = category_slug)
            products = Product.objects.filter(category = categories ,is_available = True).order_by('-created_date')
            paginator = Paginator(products,3)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()
        else:
            products = Product.objects.all().filter(is_available = True).order_by('-created_date')
            paginator = Paginator(products,8)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()
        
        context = {
            
            # 'products':products,
            'products':paged_products,
            'products_count':total_products,
        }
        return render(request, 'store/store.html' , context)
def head_phone_latest_product(request):
    category_slug = 'head-phone'
    if category_slug != None :
            
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories ,is_available = True).order_by('-created_date')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('-created_date')
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()
        
    context = {
            
            # 'products':products,
        'products':paged_products,
        'products_count':total_products,
    }
    return render(request, 'store/store.html' , context)

def mobile_phone_latest_product(request):
    category_slug = 'mobile-phone'
    categories = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category = categories ,is_available = True).order_by('-created_date')
    paginator = Paginator(products,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    total_products = products.count()
    context = {
            
            # 'products':products,
        'products':paged_products,
        'products_count':total_products,
    }
    return render(request, 'store/store.html' , context)
    
    
            
