from django.shortcuts import render
from django.http import JsonResponse
from appmart.models import Product, Category, ProductImages

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
        'price': request.GET.get('price')
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


