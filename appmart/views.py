from django.shortcuts import render, redirect
from django.http import JsonResponse
from appmart.models import Product, Category, ProductImages
from django.contrib import messages

# Create your views here.

def index(request):
    products = Product.objects.filter(featured = True, status = True)
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
    products = Product.objects.filter(category=category, status = True)

    context = {
        "category":category,
        "products":products,
    }
    return render(request, "mart/category_product_list.html",context)

def product_all_list(request):
    products = Product.objects.filter(status = True)
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



# def add_to_cart(request):
#     cart_product = {}
#     cart_product[str(request.GET['id'])] = {
#         'title' : request.GET['title'],
#         'qty' : request.GET['qty'],
#         'price' : request.GET['price']
#     }
#     if 'cart_data_obj' in request.session:
#         if str(request.GET[id]) in request.session['cart_data_obj']:
#             cart_data = request.session['cart_data_obj']
#             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
#             cart_data.update(cart_data)
#             request.session['cart_data_obj'] = cart_data
#         else:
#             cart_data = request.session['cart_data_obj']
#             cart_data.update(cart_product)
#             request.session['cart_data_obj'] = cart_data
#     else:
#         request.session['cart_data_obj'] = cart_product
#     return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})
#     # return render(request,'mart/user_cart.html')






# def add_to_cart(request):
#     cart_product = {
#         'title': request.GET.get('title'),
#         'qty': request.GET.get('qty'),
#         'price': request.GET.get('price')
#     }

#     cart_data = request.session.get('cart_data_obj', {})
#     product_id = str(request.GET.get('id'))

#     if product_id in cart_data:
#         # Update quantity if the product already exists in the cart
#         cart_data[product_id]['qty'] = int(cart_product['qty'])
#     else:
#         # Add the product to the cart
#         cart_data[product_id] = cart_product

#     request.session['cart_data_obj'] = cart_data

#     return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})




# def add_to_cart(request):
#     cart_product = {}
#     cart_product[str(request.GET['id'])] = {
#         'title' : request.GET['title'],
#         'qty' : request.GET['qty'],
#         'price' : request.GET['price']
#     }
#     if 'cart_data_obj' in request.session:
#         if str(request.GET['id']) in request.session['cart_data_obj']:

#             cart_data = request.session['cart_data_obj']
#             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
#             cart_data.update(cart_data)
#             request.session['cart_data_obj'] = cart_data
#         else:
#             cart_data = request.session['cart_data_obj']
#             cart_data.update(cart_product)
#             request.session['cart_data_obj'] = cart_data
#     else:
#         request.session['cart_data_obj'] = cart_product
#     return JsonResponse({"data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})




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



# def shop_cart_view(request):
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
#             # cart_total_amount += int(item['qty']) + float(item['price'])

#             cart_total_amount += int(item['qty']) * float(item['price'])

#         return render(request,"mart/shop-cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect("appmart:index")




# cart_total_amount = 0
# if 'cart_data_obj' in request.session:
#     for p_id, item in request.session['cart_data_obj'].items():
#         quantity = int(item.get('qty', 0))  # Get quantity, default to 0 if not present
#         price = item.get('price', '')      # Get price, default to empty string if not present

#         # Check if price is not an empty string before converting to float
#         if price and price.strip():  # Check if price is non-empty and not just whitespace
#             try:
#                 float_price = float(price)
#                 cart_total_amount += quantity * float_price
#             except ValueError:
#                 # Handle the case where the price is not convertible to a float
#                 # Log the error, skip the item, or handle it according to your app's logic
#                 pass
#         else:
#             # Handle the case where the price is empty or not present
#             # Log the error, skip the item, or handle it according to your app's logic
#             pass

#     return render(request, "mart/shop-cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
# else:
#     messages.warning(request, "Your cart is empty")
#     return redirect("appmart:index")







def shop_cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            quantity = int(item.get('qty', 0))  # Default quantity to 0 if not present
            price = item.get('price', '')
            print (item)
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

        
    #     context = {
    #     "products": products,
    #     "product_id" : pid,
    # }
        return render(request, "mart/shop-cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("appmart:index")
