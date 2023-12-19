from django.shortcuts import render, redirect, HttpResponse , get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from appadmin.forms import CreateProductForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from appmart.models import *


# Create your views here.

@never_cache
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

     return render(request, 'admintemp/admin_index.html',context)


def admin_products_list(request):
     products = Product.objects.all()
     context = {
          "products":products
     }
     return render(request,'admintemp/admin_products_list.html', context)






def admin_category_list(request):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
    return render(request,'admintemp/admin_category_list.html',context)








def admin_add_category(request):
    if request.method == 'POST':
        cat_title = request.POST.get('category_name')
        
        cat_data = Category(title=cat_title,
                            image=request.FILES.get('category_image'))
    
        cat_data.save()
    else:
        return render(request, 'admintemp/admin_add_category.html')
    
    return render(request, 'admintemp/admin_add_category.html')





def admin_category_edit(request):
    return render(request, 'admintemp/admin_category_edit.html')


def admin_category_edit(request, cid):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')

    # Using get_object_or_404 to get the Category or return a 404 response if it doesn't exist
    categories = get_object_or_404(Category, cid=cid)

    if request.method == 'POST':
        # Update the fields of the existing category object
        cat_title = request.POST.get("category_name")
        cat_image = request.FILES.get('category_image')

        # Update the category object with the new title and image
        categories.title = cat_title
        if cat_image is not None:
            categories.image = cat_image

        
        # Save the changes to the database
        categories.save()

        # Redirect to the category list page after successful update
        return redirect('appadmin:admin_category_list')

    # If the request method is GET, render the template with the category details
    context = {
        "categories_title": categories.title,
        "categories_image": categories.image,
    }

    return render(request, 'admintemp/admin_category_edit.html', context)


def delete_category(request,cid):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        category=Category.objects.get(cid=cid)
    except ValueError:
        return redirect('appadmin:admin_category_list')
    category.delete()

    return redirect('appadmin:admin_category_list')


def available_category(request,cid):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    category = get_object_or_404(Category, cid=cid)
    
    if category.is_blocked:
        category.is_blocked=False
       
    else:
        category.is_blocked=True
    category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))






def admin_add_product(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    categories = Category.objects.all()
   

    if request.method == 'POST':
        product_name= request.POST.get('title')
        product_stock= request.POST.get('stock_count')
        description= request.POST.get('description')
        max_price= request.POST.get('old_price')
        sale_price= request.POST.get('price')
        category_name= request.POST.get('category')
       
       

        category = get_object_or_404(Category, title=category_name)
        

        product = Product(
            title=product_name,
            stock=product_stock,
            category=category,
            
            description=description,
            old_price=max_price,
            price=sale_price,
            image=request.FILES['image_feild']  # Make sure your file input field is named 'product_image'
        )
        product.save()

        return redirect('appadmin:admin_products_list')
    else:
        form=CreateProductForm()
    content = {
        'categories': categories,
          
        'form': form
    }
    return render(request,'admintemp/admin_add_product.html', content)


# def admin_update_product(request,pid):
#     if not request.user.is_authenticated:
#         return HttpResponse("Unauthorized", status=401)
#     product = get_object_or_404(Product, pid=pid) 


#     if request.method == "POST":

#         title = request.POST.get('title')
#         category = request.POST.get('category')
#         old_price = request.POST.get('old_price')
#         price = request.POST.get('price')
#         description = request.POST.get('description')
#         stock = request.POST.get('stock')

#         # Update the fields of the fetched product instance
#         product.title = title
#         product.category = category
#         product.old_price = old_price
#         product.price = price
#         product.description = description
#         product.stock = stock


#         product.save()

#         return HttpResponseRedirect(reverse('appadmin:admin_products_list'))
#     else:
#         form = CreateProductForm(instance=product)
#     return render(request, 'admintemp/admin_products_details.html',{'form':form})







# def admin_update_product(request, pid):
#     if not request.user.is_authenticated:
#         return HttpResponse("Unauthorized", status=401)
    
#     product = get_object_or_404(Product, pid=pid) 

#     if request.method == "POST":
        
#         form = CreateProductForm(request.POST,instance=product)
#         if form.is_valid():
#             product=form.save(commit=False)
#             product_image = request.FILES['image']
            
#             if product_image is not None:
#                 product.image = product_image
#             product.save()
#             return HttpResponseRedirect(reverse('appadmin:admin_products_list'))
#     else:
#         form = CreateProductForm(instance=product)
#     context = {
#         'product' : product,
#         'form' : form
#     }
        
    
#     return render(request, 'admintemp/admin_products_details.html', context)



def admin_update_product(request, pid):
    # Retrieve the product instance using its ID (pid)
    product = get_object_or_404(Product, pid=pid)
    print("Hello")

    if request.method == "POST":
        print("hello")
        # Bind the product instance to the form and update it with the POST data
        form = CreateProductForm(request.POST,request.FILES, instance=product)
        title=form.cleaned_data['title']
        print(title)
        print(pid)
        if form.is_valid():
            form.save()
            # Redirect to the product details or any other desired page after successful update
            return redirect('appadmin:admin_products_list')
    else:
        # If it's a GET request, create a form instance populated with the product data
        form = CreateProductForm(instance=product)
    
    return render(request, 'admintemp/admin_products_details.html', {'form': form, 'product': product})




@login_required(login_url='appadmin:admin_login')
def block_unblock_products(request, pid):
  if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
  product = get_object_or_404(Product, pid=pid)
  if product.status:
    product.status=False
  else:
      product.status=True
  product.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request,pid):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    try:
        product = Product.objects.get(pid=pid)
        product.delete()
        return redirect('appadmin:admin_products_list')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)



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
            return render(request, 'admintemp/admin_products_details.html', context)

    else:
        form = CreateProductForm(instance=product)
        # print(form)
    context = {
        'form': form,
        'product': product,
        
    }
    return render(request, 'admintemp/admin_products_details.html', context)


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
      
    return render(request,'admintemp/users_list.html',context)

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
  


def cart_order_list(request):
    orders = CartOrder.objects.all().order_by("-order_date")
    print(orders)
    context = {
        "orders" : orders
    }
    return render(request,'admintemp/cart_order.html', context)


def admin_order_detail(request,id):

    order = get_object_or_404(CartOrder,id=id)
    product_orders = CartOrderProducts.objects.filter(order=order)

    context = {
        'order' : order,
        'product_orders' : product_orders,
    }
    return render(request,'admintemp/admin_order_detail.html',context)


# def admin_products_list(request):
#      products = Product.objects.all()
#      context = {
#           "products":products
#      }
#      return render(request,'admintemp/admin_products_list.html', context)






# def delete_order(request, order_id):
#     if request.method == 'POST':
#         order = get_object_or_404(CartOrder, id=order_id)
        
#         # Check if the selected status is 'Cancel'
#         if order.product_status == 'Cancel':
#             order.delete()
#             return JsonResponse({'message': 'Order canceled and deleted successfully.'})
#         else:
#             return JsonResponse({'message': 'Order status is not "Cancel".'}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request method.'}, status=405)




# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def delete_cart_order(request,pid):
#     if not request.user.is_authenticated:
#         return redirect('appadmin:admin_login')
#     try:
#         order = CartOrder.objects.get(id=order_id)
#         order.delete()
#         return redirect('appadmin:cart_order_list')
#     except CartOrder.DoesNotExist:
#         return HttpResponse("Order not found", status=404)


def delete_cart_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    
    try:
        order = CartOrder.objects.get(id=order_id)
        order.delete()
        return redirect('appadmin:cart_order_list')
    except CartOrder.DoesNotExist:
        return HttpResponse("Order not found", status=404)



def admin_cancel_order(request, id):
    order = get_object_or_404(CartOrder, id=id)
    user_wallet = wallet.objects.get(user=request.user)
    # user_wallet = get_object_or_404(wallet, user=request.user)
    # user_wallet, created = wallet.objects.get_or_create(user=request.user)

    if order.product_status == 'cancelled':
        messages.warning(request, f"Order {order.id} is already cancelled.")
    else:
        # Update order status to 'cancelled'
        order.product_status = 'cancelled'
        order.save()

        
        
        if order.paid_status==True:
            user_wallet.Amount+=order.price
            user_wallet.save()
            messages.warning(request,"Refund amount has been added to the wallet")
            

        # Update product stock count
        products = CartOrderProducts.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock = int(s.stock) + p.qty
                s.save()

        messages.success(request, f"Order {order.id} has been cancelled successfully.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))    

