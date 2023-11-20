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
    
    # path('add_product/',views.add_product,name='add_product'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('signup/otp_verification',views.otp_verification,name='otp_verification'),
    
]