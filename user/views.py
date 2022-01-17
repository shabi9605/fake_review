from django.shortcuts import render,redirect,get_object_or_404


from .models import *
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from product.models import *


# Create your views here.
def index(request):
    products=ProductAdd.objects.all()
    categories = Category.objects.all()

    return render(request,'index.html',{'products':products,'categories': categories})
# def baselayout(requset):
#     products=ProductAdd.objects.all()
#     return render(requset,'baselaout.html',{'products':products})


def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        Contacts.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        return render(request,'contact.html',{'msg': 'Successfully sent message'})
    return render(request,'contact.html')

def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()

            registered=True
        else:
            HttpResponse('Invalid form')
    else:
        user_form=UserForm()
        profile_form=ProfileForm()
    return render(request,'register.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                 return HttpResponse('user not active')
        else:
            return HttpResponse('invalid username or password ')

    else:
        return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('index')
def manager_dashboard(request):
    today=datetime.now()
    total_product=Product.objects.count()
    today_product=Product.objects.filter(created_on=today).count()
    customer=Register.objects.filter(user_type='customer').count()
    products=ProductAdd.objects.all()
    context = {
        'product':total_product,
        'today_product':today_product,
        'customer':customer,
        'products':products
    }
    return render(request,'manger_dashboard.html',context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.register)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('manager_dashboard')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.register)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id,
        is_available=True
    )

    return render(
        request,
        'product/detail.html',
        {'product': product}
    )
