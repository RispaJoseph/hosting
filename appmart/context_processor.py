from appmart.models import Product, Category, ProductImages, Wishlist_model

def default(request):
    categories = Category.objects.all()

    try:
        wishlist=wishlist_model.objects.filter(user=request.user)
    except:
        # messages.warning(request,"You need to login to access wishlist")
        wishlist=0

    return {
        'categories':categories,
        'wishlist':wishlist,
    }
