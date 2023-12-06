from django.shortcuts import render, redirect
from django.http import JsonResponse
from appmart.models import Product, Category, ProductImages, CartOrder, CartOrderProducts, Address
from account.models import Profile
from django.contrib import messages
from django.template.loader import render_to_string 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
# Create your views here.




# def date_time(request):
#     current_date = timezone.now().date()  # Assign the current date to 'current_date'
#     return render(request, 'payment_completed.html', {'current_date': current_date})




def index(request):
    category_block = Category.objects.filter(is_blocked=True)
    products = Product.objects.filter(featured = True, status = True).exclude(category__in=category_block)
    latest = Product.objects.all().order_by("-id")[:10]
    category = Category.objects.filter(is_blocked=False)

    
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
    products = Product.objects.filter(category=category, status = True)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "mart/category_product_list.html",context)

def product_all_list(request):
    category_block = Category.objects.filter(is_blocked=True)
    products = Product.objects.filter(status = True).exclude(category__in=category_block)
    category = Category.objects.filter(is_blocked=True)

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
    else:
        # If the product is new, add it to the cart data
        cart_data[product_id] = cart_product

    # Update the session with the modified cart data
    request.session['cart_data_obj'] = cart_data

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})





def shop_cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            quantity = int(item.get('qty', 0))  # Default quantity to 0 if not present
            price = item.get('price', '')
            
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

        return render(request, "mart/shop-cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
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
def checkout_view(request):

    cart_total_amount = 0
    total_amount = 0

    #checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session:


        # getting total amount for Paypal amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

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

    return render(request, "mart/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'paypal_payment_button': paypal_payment_button})

    


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


@login_required(login_url='account:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        orders = CartOrder.objects.filter(user=request.user).order_by("-id")
        context = {
            "orders": orders,
        }
        return render(request, 'mart/dashboard.html', context)




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




def cod(request):
    return render(request,'mart/cash_on_delivery.html')

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    current_time = timezone.now().date()
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'mart/payment_completed.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'current_time': current_time, })

                                                           


def payment_failed_view(request):
    return render(request, 'mart/payment_failed.html') 