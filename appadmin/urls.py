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
    path('users_list',views.users_list,name='users_list'),
    
    # path('add_product/',views.add_product,name='add_product'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('signup/otp_verification',views.otp_verification,name='otp_verification'),
    
]