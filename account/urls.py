from django.urls import path
from account import views
urlpatterns = [
    path('signup',views.sign_up,name='signup'),
    path('login',views.login_view,name='login'),
    path('index',views.index,name='index'),
    
]
