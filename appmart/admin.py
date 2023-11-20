from django.contrib import admin
from django.conf import settings
from account.models import User
from django.contrib.auth import get_user_model

from appmart.models import Category, Product, ProductImages
# Register your models here.

admin.site.register(get_user_model())

class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin]
  list_display = ['pid','title','product_image','price','category','featured','status','stock']
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['title', 'category_image']
  
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)