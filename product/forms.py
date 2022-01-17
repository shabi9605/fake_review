from django import forms
from django.db.models import fields
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ('name','description')


class ProductForm(forms.ModelForm):

    class Meta:
        model=ProductAdd
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=('review',)



class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields=('status',)