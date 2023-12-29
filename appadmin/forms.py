from django import forms
from appmart.models import Product, Category, ProductOffer
from appmart.models import ProductImages
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput


class CreateProductForm(forms.ModelForm):
    new_image = forms.ImageField(required=False)

            
    class Meta:
        model = Product
        fields =['title','category','old_price','price','description','stock', 'new_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_stock(self):
        stock= self.cleaned_data.get('stock')

        if stock is not None and stock < Decimal('0'):
            raise ValidationError("Stock count cannot be negative")

        return stock

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < Decimal('0'):
            raise ValidationError("Price cannot be negative")
        return price

    def clean_old_price(self):
        old_price = self.cleaned_data.get('old_price')

        if old_price is not None and old_price < Decimal('0'):
            raise ValidationError("Price cannot be negative")
        return old_price

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



class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['discount_percentage', 'start_date', 'end_date', 'active']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise forms.ValidationError('Discount percentage must be between 0 and 100.')
        return discount_percentage
    