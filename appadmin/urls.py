from django.urls import path
from appadmin import views

app_name = "appadmin"
urlpatterns = [
    # path('signup/',views.sign_up,name='signup'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('add_product/',views.add_product,name='add_product'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('signup/otp_verification',views.otp_verification,name='otp_verification'),
    
]