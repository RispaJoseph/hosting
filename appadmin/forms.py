from django import forms
from appmart.models import Product, Category

class CreateProductForm(forms.ModelForm):
    
            
    class Meta:
        model = Product
        fields =['title','category','old_price','price','description','stock']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Category
        fields = ['title', 'image'] 