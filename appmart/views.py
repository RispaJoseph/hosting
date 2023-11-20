from django.shortcuts import render
from appmart.models import Product, Category, ProductImages

# Create your views here.

def index(request):
    products = Product.objects.filter(featured = True)
    latest = Product.objects.all().order_by("-id")[:10]
    category = Category.objects.all()

    
    context = {
        "products":products,
        "latest":latest,
        "category":category
    }
    return render(request, 'mart/index.html',context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request, 'mart/category_list.html',context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category=category)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "mart/category_product_list.html",context)

def product_all_list(request):
    products = Product.objects.all()
    category = Category.objects.all()

    context = {
        "products":products,
        "category":category,
    }
    return render(request, 'mart/product_all_list.html',context)



def product_detail(request,pid):
    product = Product.objects.get(pid = pid)
    p_image =product.p_images.all()
    category = Category.objects.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    
    
    context={
        "product":product,
        "p_image":p_image,
        "category":category,
        "products":products
        
        
        
    }
    return render (request,'mart/product_detail.html',context)

