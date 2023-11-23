from django.urls import path
from appmart import views

app_name = "appmart"
urlpatterns = [
    path('',views.index,name='index'),
    path('category/',views.category_list_view,name='category'),
    path('category/<cid>',views.category_product_list_view,name='category_product_list'),
    path('product_all_list/',views.product_all_list, name='product_all_list'),
    path('product/<pid>/', views.product_detail, name = 'product-detail'),

    path('add_to_cart/', views.add_to_cart, name = 'add_to_cart'),
]