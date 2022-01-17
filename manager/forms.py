
from django import forms
from django.forms import fields
from product.models import *

class ProductAddForm(forms.ModelForm):
    class Meta:
        model=ProductAdd
        fields="__all__"
class ProductComparisonForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"
