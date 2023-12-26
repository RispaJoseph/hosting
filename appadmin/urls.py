from django.urls import path
from appadmin import views


app_name = "appadmin"
urlpatterns = [
    # path('signup/',views.sign_up,name='signup'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('admin_products_list',views.admin_products_list,name='admin_products_list'),
    path('admin_products_details/<pid>/',views.admin_products_details,name='admin_products_details'),
    path('admin_category_list',views.admin_category_list,name='admin_category_list'),
    path('admin_add_product',views.admin_add_product,name='admin_add_product'),
    path('users_list',views.users_list,name='users_list'),
    path('block_unblock_user/<int:user_id>/',views.block_unblock_user,name='block_unblock_user'),
    path('admin_add_category',views.admin_add_category,name='admin_add_category'),
    path('block_unblock_products/<str:pid>',views.block_unblock_products,name='block_unblock_products'),
    path('delete_product/<str:pid>',views.delete_product,name='delete_product'),
    # path('admin_update_product/<str:pid>/', views.admin_update_product, name='admin_update_product'),
    path('admin_category_edit/<str:cid>/',views.admin_category_edit,name="admin_category_edit"),
    path('delete_category/<str:cid>',views.delete_category,name='delete_category'),
    path('available_category/<str:cid>',views.available_category,name='available_category'),

    path('cart_order_list',views.cart_order_list,name='cart_order_list'),
    # path('delete_cart_order/<int:order_id>/',views.delete_cart_order,name='delete_cart_order'),
    path('admin_user/delete_cart_order/<int:order_id>/', views.delete_cart_order, name='delete_cart_order'),

    # admin cancel order

    path('admin-cancel-order/<int:id>',views.admin_cancel_order,name='admin-cancel-order'),

    path('admin_order_detail/<int:id>/',views.admin_order_detail,name='admin_order_detail'),



    path('admin-coupon/',views.admin_coupon, name='admin-coupon'),
    
    path('create-coupon/',views.create_coupon, name='create-coupon'),
    
    path('edit-coupon/<int:id>/',views.edit_coupon, name='edit-coupon'),
    
    path('delete-coupon/<int:id>/',views.delete_coupon, name='delete-coupon'),

    
    path('sales_report/',views.sales_report, name='sales_report'),

    path('update_product_status/<int:id>/', views.update_product_status, name='update_product_status'),

    
    # path('add_product/',views.add_product,name='add_product'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('signup/otp_verification',views.otp_verification,name='otp_verification'),
    
]