from django.shortcuts import render, redirect
from django.http import JsonResponse
from appmart.models import Product, Category, ProductImages, CartOrder, CartOrderProducts, Address, Wishlist_model, wallet, Coupon, ProductOffer, Banner
from account.models import Profile
from django.contrib import messages
from django.template.loader import render_to_string 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.template.loader import render_to_string

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
from django.core import serializers
from decimal import Decimal
from appadmin.forms import CouponForm
from django.views.decorators.cache import never_cache, cache_control

# Create your views here.




# def date_time(request):
#     current_date = timezone.now().date()  # Assign the current date to 'current_date'
#     return render(request, 'payment_completed.html', {'current_date': current_date})




def index(request):
    category_block = Category.objects.filter(is_blocked=True)
    products = Product.objects.filter(featured = True, status = True).exclude(category__in=category_block)
    latest = Product.objects.all().order_by("-id")[:10]
    category = Category.objects.filter(is_blocked=False)
    banners = Banner.objects.filter(is_active=True)



    try:
        
        discount_offer = ProductOffer.objects.get(active=True)
    except ProductOffer.DoesNotExist:
        discount_offer = None
    if discount_offer:
        current_date = timezone.now()
        if current_date > discount_offer.end_date or current_date < discount_offer.start_date:
            discount_offer.active = False
            discount_offer.save()
    

    
    context = {
        "products":products,
        "latest":latest,
        "category":category,
        "discount_offer": discount_offer,
        "banners": banners
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
    products = Product.objects.filter(category=category, status = True)
    

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "mart/category_product_list.html",context)

def product_all_list(request):
    category_block = Category.objects.filter(is_blocked=True)
    products = Product.objects.filter(status = True).exclude(category__in=category_block)
    category = Category.objects.filter(is_blocked=False)
    print(category)
    print(products)
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



# ..................................Cart updation,deletion........................................


def add_to_cart(request):
    product_id = str(request.GET.get('id'))
    cart_data = request.session.get('cart_data_obj', {})

    cart_product = {
        'title': request.GET.get('title'),
        'qty': int(request.GET.get('qty')),
        'price': request.GET.get('price'),
        'image': request.GET.get('image'),
        'pid': request.GET.get('pid'),
    }



    if product_id in cart_data:
        # If the product already exists in the cart, update its quantity
        cart_data[product_id]['qty'] += cart_product['qty']

        return JsonResponse({
            "message": "Product already in cart",
            'totalcartitems': len(request.session['cart_data_obj']),
            'already_in_cart': True
        })
    else:
        # If the product is new, add it to the cart data
        cart_data[product_id] = cart_product

    # Update the session with the modified cart data
    request.session['cart_data_obj'] = cart_data

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'already_in_cart': False, "message": "Product added to cart"})





def shop_cart_view(request):
    cart_total_amount = 0
    coupon=""
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            quantity = int(item.get('qty', 0))  # Default quantity to 0 if not present
            price = item.get('price', '')

            coupon = Coupon.objects.filter(active=True)
            
            content = {
                "coupon":coupon,
            }
            
            # products = Product.objects.get(pid = p_id)
                  # Default price to empty string if not present

            try:
                if price.strip():  # Check if the price string is not empty or only whitespace
                    float_price = float(price)
                    cart_total_amount += quantity * float_price
            except ValueError:
                # Handle the case where the price is not convertible to a float
                # Log the error, skip the item, or handle it according to your app's logic
                pass

        return render(request, "mart/shop-cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'coupon':coupon})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("appmart:index")


# def delete_item_from_cart(request):
#     product_id = str(request.GET['id'])
#     if 'cart_data_obj' in request.session:
#         if product_id in request.session['cart_data_obj']:
#             cart_data = request.session['cart_data_obj']
#             del request.session['cart_data_obj'][product_id]
#             request.session['cart_data_obj'] = cart_data

#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])

#     context = render_to_string("mart/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
#     return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})
    


def delete_item_from_cart(request):
    product_id = str(request.GET.get('id'))
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("mart/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})



def update_cart(request):
    product_id = str(request.GET.get('id'))
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("mart/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})



@login_required
# @never_cache
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout_view(request):

    cart_total_amount = 0
    total_amount = 0
    final_money = 0
    money = 0 
   
    

    #checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session:


        # getting total amount for Paypal amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
            products=Product.objects.filter(title=item['title'])
            for p in products:
                if int(p.stock) < int(item['qty']):
                    messages.warning(request,f"{item['qty']} quantity not available")
                    return redirect("appmart:shop_cart_view")

    

        # create order objects
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount
        )

        # Gettting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderProducts.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])
                
                
            )



   
   
            # coupon
            if request.method == 'POST':
                coupon_form = CouponForm(request.POST)  # Instantiate the coupon form with the POST data

                if coupon_form.is_valid():
                    coupon_code = coupon_form.cleaned_data['code']
                    print(coupon_code)
                    
                    try:
                        # Assuming you have a Coupon model
                        coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
                        
                        # Check if the coupon is within its active and expiry dates
                        current_date = timezone.now().date()
                        if current_date < coupon.active_date or current_date > coupon.expiry_date:
                            messages.warning(request, 'Invalid coupon code or expired')
                        else:
                            # Apply the coupon discount to the cart total
                            money=total_amount
                            cart_total_amount -= (cart_total_amount* coupon.discount) / 100
                            request.session['applied_coupon'] = cart_total_amount
                            final_money=money-cart_total_amount
                            print(final_money)
                            messages.success(request, f'Coupon "{coupon.code}" applied successfully')

                    except Coupon.DoesNotExist:
                        messages.warning(request, 'Invalid coupon code')
            else:
                coupon_form = CouponForm()
            # coupon end

    

    host = request.get_host()
    paypal_dict = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' : cart_total_amount,
        'item_name' : "Order-Item-No-" + str(order.id),
        'invoice' : "INVOICE_NO-" + str(order.id),
        'currency_code' : "USD",
        'notify_url' : 'http://{}{}'.format(host, reverse("appmart:paypal-ipn")),
        'return_url' : 'http://{}{}'.format(host, reverse("appmart:payment-completed")),
        'cancel_url' : 'http://{}{}'.format(host, reverse("appmart:payment-failed")),

    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         cart_total_amount += int(item['qty']) * float(item['price'])

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        messages.warning(request, "Activated or Add your address")
        # active_address = None
        return redirect('appmart:dashboard')
    return render(request, "mart/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'paypal_payment_button': paypal_payment_button, "active_address":active_address, "coupon_form":coupon_form,"final_money":final_money, "money":money})

    


# @login_required(login_url='account:login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login') 
#     else:
#         return render(request, 'mart/dashboard.html')

#     profile = Profile.objects.get(user=request.user)
#     print(request.user)

#     context = {
#         "profile": profile,
#     }



# @login_required(login_url='account:login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login') 
#     else:        
#         return render(request, 'mart/dashboard.html')

#     orders = CartOrder.objects.filter(user=request.user)
#     context = {
#         "orders" : orders,
#     }
#     return render(request, 'mart/dashboard.html', context)


# @login_required(login_url='account:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to access Dashboard.")
        return redirect('appmart:index')
    else:
        orders = CartOrder.objects.filter(user=request.user).order_by("-id")
        address = Address.objects.filter(user=request.user)

        
        
        if request.method == "POST":
            address = request.POST.get("address")
            mobile = request.POST.get("phone")

            new_address = Address.objects.create(
                user = request.user,
                address = address,
                mobile = mobile,
            )
            messages.success(request, "Address Added Successfully.")
            return redirect("appmart:dashboard")
        else: 
            print("Error")

        user_profile, created = Profile.objects.get_or_create(user=request.user)

        print("user profile is : ", user_profile)

        wallet_amount = wallet.objects.filter(user=request.user)

        context = {
            "user_profile": user_profile,
            "orders": orders,
            "address" : address,
            "wallet_amount": wallet_amount,
        }
        return render(request, 'mart/dashboard.html', context)


# def make_address_default(request):
#     id =request.GET['id']
#     Address.objects.update(status=False)
#     Address.objects.filter(id =id).update(status=True)
#     return JsonResponse({'boolean':True})

def make_address_default(request):
    id = request.GET.get('id')
    if id:
        Address.objects.update(status=False)
        Address.objects.filter(id=id).update(status=True)
        return JsonResponse({'boolean': True})
    else:
        return JsonResponse({'boolean': False})




def order_details(request,id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)
    context = {
            "order_items": order_items,
        }
    return render(request, 'mart/order-detail.html', context)




def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        "products" : products,
        "query" : query
    }
    return render(request, 'mart/search.html', context)



@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cod(request):
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock=int(p.stock) - int(item['qty'])
                p.save() 

        del request.session['cart_data_obj']
    else:
        return redirect("appmart:index")

    return render(request,'mart/cash_on_delivery.html')





@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    total_amount=0
# stock count mgt
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock=int(p.stock) - int(item['qty'])
                p.save()
    # id = request.GET['id']
    # orders = CartOrder.objects.filter(id=id)
    # print(orders)
    latest_order = CartOrder.objects.filter(user=request.user).order_by('-order_date').first()
    latest_order.paid_status=True
    latest_order.save()
    print(latest_order)

    current_time = timezone.now().date()
    if 'cart_data_obj' in request.session:

        applied_coupon = request.session.get('applied_coupon',None)
        if applied_coupon is not None:
            cart_total_amount = applied_coupon
            
            del request.session['applied_coupon']
        else:
            cart_total_amount = 0
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
                discount = total_amount-cart_total_amount
        
        del request.session['cart_data_obj']
    return render(request, 'mart/payment_completed.html', {"cart_data": cart_data, 'totalcartitems': len(cart_data), 'cart_total_amount': cart_total_amount, 'current_time': current_time,'total_amount':total_amount,'discount':discount })

                                                           


def payment_failed_view(request):
    return render(request, 'mart/payment_failed.html') 



def wishlist_view(request):
    wishlist = Wishlist_model.objects.filter(user=request.user)
    print(wishlist)
    
    context = {
        "w":wishlist
    }
    return render(request,'mart/wishlist.html', context)







def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print("product id iss:" + product_id)

    context = {}
    wishlist_count = Wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool":True
        }
    else:
        new_wishlist = Wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool" : True
        }

    return JsonResponse(context)





# def add_to_wishlist(request):
#     if request.user.is_authenticated:  # Check if the user is logged in
#         product_id = request.GET.get('id')  # Use get() to avoid KeyError if 'id' is missing

#         if product_id:
#             product = Product.objects.get(id=product_id)

#             context = {}
#             wishlist_count = Wishlist_model.objects.filter(product=product, user=request.user).count()
#             print(wishlist_count)

#             if wishlist_count > 0:
#                 context = {
#                     "bool": True
#                 }
#             else:
#                 new_wishlist = Wishlist_model.objects.create(
#                     product=product,
#                     user=request.user
#                 )
#                 context = {
#                     "bool": True
#                 }

#             return JsonResponse(context)
#         else:
#             return JsonResponse({"error": "Product ID is missing"})
#     else:
#         return JsonResponse({"error": "User is not authenticated"})





# def remove_wishlist(request):
#     pid = request.GET['id']
#     wishlist = Wishlist_model.objects.filter(user=request.user)

#     product = Wishlist_model.objects.get(id=pid)
#     product.delete()

#     context = {
#         "bool" : True,
#         "wishlist" : wishlist
#     }
#     data = render_to_string("mart/wishlist-list.html", context)
#     return JsonResponse({"data":data, "w":wishlist})



def remove_wishlist(request):
    pid =request.GET['id']
    wishlist= Wishlist_model.objects.filter(user=request.user)
    
    wishlist_d=Wishlist_model.objects.get(id=pid)
    
    delete_product=wishlist_d.delete()
    
    context={
        "bool":True,
        "w":wishlist
        
    }
    if not wishlist_d:
        messages.warning(request,"Nothiing")
    
    
    wishlist_json=serializers.serialize('json', wishlist)
    data= render_to_string("mart/wishlist-list.html", context)
    
    
    return JsonResponse({"data":data,"w":wishlist_json})



def wallet_view(request):
    total_amount = 0
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            print(item)
            products=Product.objects.filter(title=item['title'])
            for p in products:
                p.stock=int(p.stock) - int(item['qty'])
                p.save() 

    #create wallet
    user_wallet, created = wallet.objects.get_or_create(user=request.user)

    print(user_wallet.Amount)


    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        print(cart_data)
        applied_coupon = request.session.get('applied_coupon',None)
        if applied_coupon is not None:
            total_amount = applied_coupon
            
            del request.session['applied_coupon']

        else:
            total_amount = 0
            for p_id, item in cart_data.items():
                # try:
                #     # Split the price string into individual prices and convert to float
                #     prices = [float(price) for price in item.get('price', '').split()]
                #     # Sum up the individual prices
                #     total_price = sum(prices)
                #     qty = int(item.get('qty', 0))
                #     total_amount += qty * total_price
                # except (ValueError, TypeError):
                #     # Handle conversion errors if qty or total_price is not a valid number
                #     pass


                for p_id, item in request.session['cart_data_obj'].items():
                    total_amount += int(item['qty']) * float(item['price'])

        total_amount_decimal = Decimal(str(total_amount))

        if user_wallet.Amount < total_amount:
            messages.error(request, "Wallet money is not enough to purchase this product")
            return redirect("appmart:checkout")
        else:
            user_wallet.Amount-=total_amount_decimal
            user_wallet.save()
            messages.success(request,f"{total_amount_decimal} has been deducted from your wallet" )

        latest_order = CartOrder.objects.filter(user=request.user).order_by('-order_date').first()
        latest_order.paid_status=True
        latest_order.save()
        print(latest_order)

    del request.session['cart_data_obj']
    return render(request,'mart/cash_on_delivery.html')


# def filter_product(request):    
#     # try:
#             categories = request.GET.getlist('category[]')
#             # print("Selected Categories:", categories)

#             # min_price= request.GET['min_price']
#             # max_price= request.GET['max_price']
            
#             products = Product.objects.filter(status=True).order_by('-id').distinct()
            
#             # products=products.filter(price__gte=min_price)
#             # products=products.filter(price__lte=max_price)
#             # print("All Products:", products)
#             # print("Selected Categories:", categories)

#             if len(categories) > 0:
#                 products = products.filter(category__cid__in=categories).distinct()
#                 # print("Filtered Product:", products)

#             data = render_to_string('appmart/product-list.html', {"products": products})
#             return JsonResponse({"data": data})
#     # except Exception as e:
#             # return JsonResponse({"error": str(e)})



def filter_product(request):    
    try:
        categories = request.GET.getlist('category[]')
        print("Selected Categories:", categories)
        

        min_price= request.GET['min_price']
        max_price= request.GET['max_price'] 

        products = Product.objects.filter(status=True).order_by('-id').distinct()
        
        products=products.filter(price__gte=min_price)
        products=products.filter(price__lte=max_price)
        print("All Products:", products)
        print("Selected Categories:", categories)

        if len(categories) > 0:
            products = products.filter(category__cid__in=categories).distinct()
            print("Filtered Product :", products)

        data = render_to_string('mart/product-list.html', {"products": products})
        return JsonResponse({"data": data})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    

    