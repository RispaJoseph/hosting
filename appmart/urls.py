from django.urls import path, include
from appmart import views


app_name = "appmart"
urlpatterns = [
    path('',views.index,name='index'),
    path('category/',views.category_list_view,name='category'),
    path('category/<cid>',views.category_product_list_view,name='category_product_list'),
    path('product_all_list/',views.product_all_list, name='product_all_list'),
    path('product/<pid>/', views.product_detail, name = 'product-detail'),

    path('add_to_cart/', views.add_to_cart, name = 'add_to_cart'),
    path('shop_cart_view/', views.shop_cart_view, name = 'shop_cart_view'),
    path('delete-from-cart/', views.delete_item_from_cart, name = 'delete-from-cart'),
    path('update-cart/', views.update_cart, name = 'update-cart'),    
    path('checkout/',views.checkout_view,name='checkout'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('cod/',views.cod,name='cod'),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-completed/',views.payment_completed_view,name='payment-completed'),
    path('payment-failed/',views.payment_failed_view,name='payment-failed'),
    path('search_view/',views.search_view,name='search_view'),
    path('dashboard/order/<int:id>',views.order_details,name='order_details'),

    path('wishlist/',views.wishlist_view,name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/', views.remove_wishlist, name='remove-from-wishlist'),

    path('make-default-address/', views.make_address_default, name='make-default-address'),

    path('wallet-view/', views.wallet_view, name='wallet-view'),

    path('filter-product/', views.filter_product,name='filter-product'),

   

 

    

]