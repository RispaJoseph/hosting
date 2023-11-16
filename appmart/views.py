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