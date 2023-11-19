from django.shortcuts import render, redirect, HttpResponse , get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from appadmin.forms import CreateProductForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from appmart.models import *

# Create your views here.

def admin_login(request):
    
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
       
            user = authenticate(request,username=email,password=password)
            if user is not None and user.is_active:
                login(request,user)
                return redirect('appadmin:dashboard')
        return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('appadmin:admin_login') 


def dashboard(request):
     if not request.user.is_authenticated:
          return redirect('adminapp:admin_login')
     
     product_count = Product.objects.count()
     category_count = Category.objects.count()

     context = {
          'product_count':product_count,
          'category_count':category_count
     }

     return render(request, 'admin/admin_index.html',context)


def admin_products_list(request):
     products = Product.objects.all()
     context = {
          "products":products
     }
     return render(request,'admin/admin_products_list.html', context)


def admin_products_details(request, pid):
    print(pid)
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')

    try:
        product = Product.objects.get(pid=pid)
       
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('appadmin:admin_products_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'product': product,
                
            }
            return render(request, 'admin/admin_products_details.html', context)

    else:
        form = CreateProductForm(instance=product)
        # print(form)
    context = {
        'form': form,
        'product': product,
        
    }
    return render(request, 'admin/admin_products_details.html', context)


@login_required(login_url='appadmin:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    if not request.user.is_authenticated:
        return redirect('admin:admin_login')
    
    search_query=request.GET.get('query')

    if search_query:
         users = User.objects.filter(username__icontains=search_query)
    else:
         users = User.objects.all()
         print("the users are :", users)
    context = {
        'users': users
    }
      
    return render(request,'admin/users_list.html',context)

@login_required(login_url='appadmin:admin_login')
def block_unblock_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    user = get_object_or_404(User, id=user_id)
    
    if user.is_active:
        
        user.is_active=False
        
    else:
        user.is_active=True
        
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
  


# def add_product(request):
#     if request.method=='POST':
#          title=request.POST.get('title')
#          description=request.POST.get('description')
#          price=request.POST.get('price')
#          old_price=request.POST.get('old_price')
#          stock=request.POST.get('stock')
#          image=request.FILES['image']
#          print(title)
#          product_data=Product(title=title,description=description,price=price,old_price=old_price,stock=stock,image=image)
#          product_data.save()
#          print(title)
#          print(product_data)
#          return redirect ('login')
    
#     return render(request,'add_product.html')