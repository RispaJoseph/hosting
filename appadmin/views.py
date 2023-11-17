from django.shortcuts import render

# Create your views here.

def admin_login(request):
    return render(request, 'admin_login.html')


def add_product(request):
    return render(request,'add_product.html')