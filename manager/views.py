from django.shortcuts import render
from .forms import *
from product.models import *
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
# Create your views here.

def manager_form(request):
    return render(request,'comparison_form.html')

def comparison_table(request):
    compare_products=Product.objects.all()
    return render(request,'comparison_table.html',{'com_products':compare_products})
    
def productadd_table(request):
    products=ProductAdd.objects.all()
    return render(request,'product_table.html',{'com_products':products})

def product_add(request,id):
    Update = ProductAdd.objects.get(id=id)
    print(Update)
    form= ProductAddForm(instance=Update)
    if request.method=='POST':
        form= ProductAddForm(request.POST,request.FILES,instance=Update)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Update succefully')
            return render(request,'manger_dashboard.html',{'form':form,'product':Update})
    return render(request,'product_add.html',{'form':form,'product':Update})

def compare_update(request,id):
    Update = Product.objects.get(id=id)
    print(Update)
    form= ProductComparisonForm(instance=Update)
    if request.method=='POST':
        form= ProductComparisonForm(request.POST,request.FILES,instance=Update,)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Update succefully')
            return render(request,'manger_dashboard.html',{'form':form,'product':Update})
    return render(request,'update_comparison.html',{'form':form,'product':Update})

def delete_product_compare(request,id):
    deleteproduct = Product.objects.get(id=id)
    deleteproduct.delete()
    messages.success(request,'Record deleted succefully')
    return render(request,'comparison_table.html')

# def delete_product(request,id):
#     deleteproductadd = ProductAdd.objects.get(id=id)
#     deleteproductadd.delete()
#     messages.success(request,'Record deleted succefully')
#     return render(request,'comparison_table.html')