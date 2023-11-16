from django.urls import path
from appmart import views

app_name = "appmart"
urlpatterns = [
    path('',views.index,name='index'),
]