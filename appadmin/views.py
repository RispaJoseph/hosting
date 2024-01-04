from django.shortcuts import render, redirect, HttpResponse , get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from appadmin.forms import CreateProductForm, CategoryForm, ProductOfferForm, BannerForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from appmart.models import *
from appadmin.models import *
from decimal import Decimal
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Avg
from datetime import datetime,timedelta
from django.utils import timezone
from django.utils.timezone import make_aware

from django.db.models.functions import TruncMonth, TruncYear

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





@login_required(login_url='appadmin:admin_login')
def dashboard(request):
     if not request.user.is_superadmin:
          return redirect('appadmin:admin_login')
     
     product_count = Product.objects.count()
     category_count = Category.objects.count()
     order_count = CartOrder.objects.count()
    #  orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    #  orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    #  month = []
    #  total_orders = []

    #  for i in orders:
    #      month.append(calendar.month_name[i["month"]])
    #      total_orders.append(i["count"])

     orders = CartOrder.objects.all()
     last_orders = CartOrder.objects.order_by('-order_date')[:5]
     orders_count = orders.count()
     total_users_count = User.objects.count()
     total = 0

     for order in orders:
         if order.product_status == 'Delivered':
             total += order.price  
         if order.paid_status:
             total += order.price  
     revenue=int(total)
     end_date = datetime.now()
     start_date = end_date - timedelta(days=7)

     daily_order_counts = (
         CartOrder.objects
         .filter(order_date__range=(start_date, end_date), paid_status=True)
         .values('order_date')
         .annotate(order_count=Count('id'))
         .order_by('order_date')
     )

     dates = [entry['order_date'].strftime('%Y-%m-%d') for entry in daily_order_counts]
     counts = [entry['order_count'] for entry in daily_order_counts]
   
    
     monthly_order_counts = (
         CartOrder.objects
         .filter(order_date__year=datetime.now().year, paid_status=True)  # Filter by current year and paid orders
         .annotate(month=TruncMonth('order_date'))
         .values('month')
         .annotate(order_count=Count('id'))
         .order_by('month')
     )

     monthly_dates = [entry['month'].strftime('%Y-%m') for entry in monthly_order_counts]
     monthly_counts = [entry['order_count'] for entry in monthly_order_counts]

     # Fetch yearly order counts and their respective dates
     yearly_order_counts = (
         CartOrder.objects
         .annotate(year=TruncYear('order_date'))
         .values('year')
         .annotate(order_count=Count('id'))
         .order_by('year')
     )

     yearly_dates = [entry['year'].strftime('%Y') for entry in yearly_order_counts]
     yearly_counts = [entry['order_count'] for entry in yearly_order_counts]

     # statuses = ['Delivered', 'Processing', 'Cancelled', 'Return','Shipped']
     # order_counts = [CartOrder.objects.filter(product_status=status).count() for status in statuses]
     statuses = ['Delivered', 'Processing', 'Cancelled', 'Return', 'Shipped']

     order_counts = (
         CartOrder.objects
         .filter(product_status__in=statuses)
         .values('product_status')
         .annotate(count=Count('id'))
         .order_by('product_status')
     )
     status_list = [entry['product_status'] for entry in order_counts]
     count_list = [entry['count'] for entry in order_counts]


     context = {
          'product_count':product_count,
          'category_count':category_count,
          'order_count':order_count,
          'dates':dates,
          'counts':counts,
          'monthlyDates':monthly_dates,
          'monthlyCounts':monthly_counts,
          'yearlyDates':yearly_dates,
          'yearlyCounts':yearly_counts,
          'last_orders':last_orders,
          'revenue':revenue,
          'total_users_count':total_users_count,
          'status_list':status_list,
          'count_list':count_list

     }

     return render(request, 'admintemp/admin_index.html',context)

@login_required(login_url='appadmin:admin_login')
def admin_products_list(request):
     products = Product.objects.all()
     context = {
          "products":products
     }
     return render(request,'admintemp/admin_products_list.html', context)





@login_required(login_url='appadmin:admin_login')
def admin_category_list(request):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
    return render(request,'admintemp/admin_category_list.html',context)







@login_required(login_url='appadmin:admin_login')
def admin_add_category(request):
    if request.method == 'POST':
        cat_title = request.POST.get('category_name')
        
        cat_data = Category(title=cat_title,
                            image=request.FILES.get('category_image'))
    
        cat_data.save()
    else:
        return render(request, 'admintemp/admin_add_category.html')
    
    return render(request, 'admintemp/admin_add_category.html')




@login_required(login_url='appadmin:admin_login')
def admin_category_edit(request):
    return render(request, 'admintemp/admin_category_edit.html')

@login_required(login_url='appadmin:admin_login')
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

@login_required(login_url='appadmin:admin_login')
def delete_category(request,cid):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    try:
        category=Category.objects.get(cid=cid)
    except ValueError:
        return redirect('appadmin:admin_category_list')
    category.delete()

    return redirect('appadmin:admin_category_list')

@login_required(login_url='appadmin:admin_login')
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





@login_required(login_url='appadmin:admin_login')
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
       

        
        try:
            product_stock = int(product_stock)
            if product_stock < 0:
                messages.warning(request,"Stock Count can't be less than Zero")
                return redirect('appadmin:admin_products_list')
            
            max_price = float(max_price)
            if max_price < 0:
                messages.warning(request,"Max Price can't be less than Zero")
                return redirect('appadmin:admin_products_list')

            sale_price = float(sale_price)
            if sale_price < 0:
                messages.warning(request,"Price can't be less than Zero")
                return redirect('appadmin:admin_products_list')
        except ValueError as e:
            messages.warning(request,str(e))
            return redirect('appadmin:admin_products_list')



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
          
        'form': form,
        
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

########################################################################
# @login_required(login_url='appadmin:admin_login')
# def admin_update_product(request, pid):
#     # Retrieve the product instance using its ID (pid)
#     product = get_object_or_404(Product, pid=pid)
#     print(product)

#     if request.method == "POST":
#         print("request.POST")
#         # Bind the product instance to the form and update it with the POST data
#         form = CreateProductForm(request.POST,request.FILES, instance=product)
#         title=form.cleaned_data['title']
#         print(title)
#         print(pid)
#         if form.is_valid():
#             form.save()
#             # Redirect to the product details or any other desired page after successful update
#             return redirect('appadmin:admin_products_list')
#         else:
#             print(form.errors)
#     else:
#         # If it's a GET request, create a form instance populated with the product data
#         form = CreateProductForm(instance=product)
    
#     return render(request, 'admintemp/admin_products_details.html', {'form': form, 'product': product})
##############################################################################################################



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



@login_required(login_url='appadmin:admin_login')
def admin_products_details(request, pid):
    print(pid)
    if not request.user.is_superadmin:
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
  

@login_required(login_url='appadmin:admin_login')
def cart_order_list(request):
    orders = CartOrder.objects.all().order_by("-order_date")
    print(orders)
    context = {
        "orders" : orders
    }
    return render(request,'admintemp/cart_order.html', context)

@login_required(login_url='appadmin:admin_login')
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

@login_required(login_url='appadmin:admin_login')
def delete_cart_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    
    try:
        order = CartOrder.objects.get(id=order_id)
        order.delete()
        return redirect('appadmin:cart_order_list')
    except CartOrder.DoesNotExist:
        return HttpResponse("Order not found", status=404)


@login_required(login_url='appadmin:admin_login')
def admin_cancel_order(request, id):
    order = get_object_or_404(CartOrder, id=id)
    # user_wallet = wallet.objects.get(user=request.user)
    user_wallet, created = wallet.objects.get_or_create(user=request.user)

    # user_wallet = get_object_or_404(wallet, user=request.user)
    # user_wallet, created = wallet.objects.get_or_create(user=request.user)

    if order.product_status == 'cancelled':
        messages.warning(request, f"Order {order.id} is already cancelled.")
    else:
        # Update order status to 'cancelled'
        order.product_status = 'cancelled'
        order.save()

        
        
        # if order.paid_status==True:
        #     user_wallet.Amount+=order.price
        #     user_wallet.save()
        #     messages.warning(request,"Refund amount has been added to the wallet")
            
        if order.paid_status == True:
            refund_amount = Decimal(order.price)  # Convert the float to Decimal
            user_wallet.Amount += refund_amount
            user_wallet.save()
            messages.warning(request, "Refund amount has been added to the wallet")

        # Update product stock count
        products = CartOrderProducts.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock = int(s.stock) + p.qty
                s.save()

        messages.success(request, f"Order {order.id} has been cancelled successfully.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))    



@login_required(login_url='appadmin:admin_login')
def admin_coupon(request):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    coupon=Coupon.objects.all()
    
    
    context={
        'coupon':coupon
    }
    return render(request,'admintemp/admin-coupon.html',context)

@login_required(login_url='appadmin:admin_login')
def create_coupon(request):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'appadmin/create-coupon.html')

        # Check if the coupon with the same code already exists
        if Coupon.objects.filter(code=code).exists():
            messages.error(request, f'Coupon with code {code} already exists')
            return render(request, 'appadmin/create-coupon.html')

        coupon = Coupon(
            code=code,
            discount=discount,
            active=active,
            active_date=active_date,
            expiry_date=expiry_date
        )
        coupon.save()
        messages.success(request, 'Coupon created successfully')
        return redirect('appadmin:admin-coupon')

    return render(request, 'admintemp/create-coupon.html')


@login_required(login_url='appadmin:admin_login')
def edit_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    
    coupon_code = get_object_or_404(Coupon, id=id)
    print(f'Active Date: {coupon_code.active_date}')
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        active_date = request.POST['active_date']
        expiry_date = request.POST['expiry_date']
        

        # Check if active_date is not greater than expiry_date
        if active_date > expiry_date:
            messages.error(request, 'Active date should not be greater than expiry date')
            return render(request, 'admintemp/create-coupon.html')
        
        coupon_code.code=code
        coupon_code.discount=discount
        coupon_code.active_date=active_date
        coupon_code.expiry_date=expiry_date
        coupon_code.active=active
        coupon_code.save()
        messages.success(request, 'Coupon Updated successfully')
        return redirect('appadmin:admin-coupon')
    
        
    
    return render (request, 'admintemp/edit-coupon.html',{'coupon_code':coupon_code})


@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_coupon(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        coupon= get_object_or_404(Coupon, id=id)
    except ValueError:
        return redirect('appadmin:admin-coupon')
    coupon.delete()
    messages.warning(request,"Coupon has been deleted successfully")

    return redirect('appadmin:admin-coupon')



# def sales_report(request):
#     return render(request,'admintemp/sales_report.html')



def sales_report(request):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    start_date_value = ""
    end_date_value = ""
    orders = CartOrder.objects.filter(product_status='delivered').order_by('-order_date')

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            
            orders = CartOrder.objects.filter(order_date__range=(start_date, end_date), product_status='delivered').order_by('-order_date')
            print(orders)
            print("hello")

    context = {
        'orders': orders,
        'start_date_value': start_date_value,
        'end_date_value': end_date_value
    }

    return render(request, 'admintemp/sales_report.html', context)


# ............Processing, Shipped, Delivered, Cancelled..............................

@login_required(login_url='appadmin:admin_login')   
def update_product_status(request, id):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    if request.method == 'POST':
        new_status = request.POST.get('product_status')
        order = get_object_or_404(CartOrder, id=id)
        order.product_status = new_status
        order.save()
        
        products = CartOrderProducts.objects.filter(order=order)
        for p in products:
            productss = Product.objects.filter(title=p.item)
            for s in productss:
                s.stock = int(s.stock) + p.qty
                s.save()
        

    # Redirect back to the original page or a specific URL
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))





# ...............................Product offer..................................................


def product_offers(request):
    offers=ProductOffer.objects.all()
    try:
        product_offer = ProductOffer.objects.get(active=True)
        print(product_offer)
    except ProductOffer.DoesNotExist:
       
        product_offer = None
    
    products = Product.objects.all()

    for p in products:
       
        if product_offer:
           
            discounted_price = p.old_price - (p.old_price * product_offer.discount_percentage / 100)
            p.price = max(discounted_price, Decimal('0.00'))  # Ensure the price is not negative
        else:
            
            p.price = p.old_price

        p.save()

    
    context={
        'offers':offers
    }
    return render(request, 'admintemp/product_offer.html',context)



def edit_product_offers(request, id):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    
    offer_discount = get_object_or_404(ProductOffer, id=id)
    print(f'Active Date: {offer_discount.start_date}')

    if request.method == 'POST':
        discount = request.POST['discount']
        active = request.POST.get('active') == 'on'
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        if end_date and start_date and end_date < start_date:
            messages.error(request, 'Expiry date must not be less than the start date.')
        else:
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

            current_date = timezone.now()
            if start_date and end_date and (current_date < start_date or current_date > end_date):
                active = False
                messages.error(request, 'Offer cannot be activated now. Check the start date.')

           
            if active:
                ProductOffer.objects.exclude(id=offer_discount.id).update(active=False)

            offer_discount.discount_percentage = discount or None
            offer_discount.start_date = start_date or None
            offer_discount.end_date = end_date or None
            offer_discount.active = active
            offer_discount.save()

            messages.success(request, 'Offer Updated successfully')
            return redirect('appadmin:product_offers')
    
    return render(request, 'admintemp/edit_product_offers.html', {'offer_discount': offer_discount})
        
            



def create_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            discount_percentage = form.cleaned_data['discount_percentage']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            active = form.cleaned_data['active']
            
            if end_date and start_date and end_date < start_date:
                messages.error(request, 'Expiry date must not be less than the start date.')
            else:
                
                current_date = timezone.now()
                if start_date and end_date and (current_date < start_date or current_date > end_date):
                    active = False
                    messages.error(request, 'Offer cannot be activated now. Check the start date.')

                if active:
                    ProductOffer.objects.update(active=False)

            # Check if any of the fields are filled
                if discount_percentage or start_date or end_date or active:
               
                    form.save()
            
            return redirect('appadmin:product_offers')  # Redirect to a view displaying the list of product offers
    else:
        form = ProductOfferForm()

    return render(request, 'admintemp/create-product-offers.html', {'form': form})


@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product_offer(request,id):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    
    try:
        offer= get_object_or_404(ProductOffer, id=id)
    except ValueError:
        return redirect('appadmin:product_offers')
    offer.delete()
    messages.warning(request,"Offer has been deleted successfully")

    return redirect('appadmin:product_offers')




# ................................Banner management..................................................

@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def banner_list(request):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    banners = Banner.objects.all()
    print(banners)
    
    return render(request, 'admintemp/admin_banner.html', {'banners':banners})


@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_banner(request):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('appadmin:banner_list')  
    else:
        form = BannerForm()
    return render(request, 'admintemp/banner_create.html', {'form': form})



@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_banner(request, id):
    if not request.user.is_superadmin:
        return redirect('appadmin:admin_login')
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('appadmin:banner_list')  # Redirect to the banners list page
    else:
        form = BannerForm(instance=banner)
    return render(request, 'admintemp/banner_update.html', {'form': form, 'banner': banner})


# def delete_banner(request, banner_id):
#     banner = get_object_or_404(Banner, pk=banner_id)
#     if request.method == 'POST':
#         banner.delete()
#         return HttpResponseRedirect('/banners/')  # Redirect to the banners list page
#     return render(request, 'delete_banner.html', {'banner': banner})


@login_required(login_url='appadmin:admin_login')        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_banner(request,id):
    if not request.user.is_superadmin:
        return redirect('adminside:admin_login')
    
    try:
        banner= get_object_or_404(Banner, id=id)
    except ValueError:
        return redirect('appadmin:banner_list')
    banner.delete()
    messages.warning(request,"Banner has been deleted successfully")

    return redirect('appadmin:banner_list')