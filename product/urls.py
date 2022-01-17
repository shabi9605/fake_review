from os import name
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('price',views.price,name='price'),
    path('category_list',views.category_list,name='category_list'),
    path('product_list1',views.product_list1,name='product_list1'),
    path('product',views.product,name='product'),
    path('categorysearch/<int:id>',views.categorysearch,name='categorysearch'),
    path('product_search', views.product_search, name='product_search'),
    path('product_detail<int:id>',views.product_detail, name='product_detail'),
    path('pre',views.predict,name='pre'),
    path('our_product',views.our_product,name='our_product'),

    path('add_review/<int:id>',views.add_review,name='add_review'),

    path('report_product/<int:id>',views.report_product,name='report_product'),

    path('view_reports',views.view_reports,name='view_reports'),
    path('verify_report/<int:id>',views.verify_report,name='verify_report'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)