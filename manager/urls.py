from django.urls import path
from .import views
urlpatterns=[
    path('manager_forms',views.manager_form,name='manager_forms'),
    path('product_add/<int:id>',views.product_add,name='product_add'),
    path('comparison_table',views.comparison_table,name='comparison_table'),
    path('compare_update/<int:id>',views.compare_update,name='compare_update'),
    path('delete_product_compare/<int:id>',views.delete_product_compare,name ='delete_product_compare'),
    path('product_table',views.productadd_table,name='product_table'),





]