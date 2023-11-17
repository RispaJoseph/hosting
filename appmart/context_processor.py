from appmart.models import Product, Category, ProductImages

def default(request):
    categories = Category.objects.all()

    return {
        'categories':categories,
    }