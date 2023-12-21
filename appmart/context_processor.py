from appmart.models import Product, Category, ProductImages, Wishlist_model
from django.db.models import Min, Max


def default(request):
    categories = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"),Max('price'))

    try:
        wishlist=wishlist_model.objects.filter(user=request.user)
    except:
        # messages.warning(request,"You need to login to access wishlist")
        wishlist=0

    return {
        'categories':categories,
        'wishlist':wishlist,
        "min_max_price":min_max_price,
    }
