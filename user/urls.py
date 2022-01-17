from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('register',views.register,name="register"),
    path('user_login',views.user_login,name="user_login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('product_detail<int:id>',views.product_detail, name='product_detail'),
    path('profile/',views.profile, name='profile'),
    path('manager_dashboard',views.manager_dashboard,name='manager_dashboard'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)