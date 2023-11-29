from django.contrib import admin
from django.conf import settings
from account.models import User, Profile
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe


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
  
  def display_category_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')

class ProfileAdmin(admin.ModelAdmin):
  list_display = ['full_name','bio','phone','image']

  

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)