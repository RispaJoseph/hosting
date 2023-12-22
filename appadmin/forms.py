from django import forms
from appmart.models import Product, Category
from appmart.models import ProductImages

class CreateProductForm(forms.ModelForm):
    new_image = forms.ImageField(required=False)
            
    class Meta:
        model = Product
        fields =['title','category','old_price','price','description','stock', 'new_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['Images']


class CategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Category
        fields = ['title', 'image'] 



class CouponForm(forms.Form):
    code = forms.CharField(max_length=50)