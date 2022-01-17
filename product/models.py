from django.db import models
from datetime import datetime

from numpy import mod
from numpy.core.numeric import ones
from user.models import *
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50,db_index=True)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='category')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

   
# class Product(models.Model):
#     category=models.ForeignKey(Category,on_delete=models.CASCADE)
#     name=models.CharField(max_length=50,db_index=True)
#     slug = models.SlugField(max_length=200, db_index=True)
#     photo=models.ImageField(upload_to='product_image/%Y/%m/%d')
#     price=models.PositiveIntegerField()
#     description=models.CharField(max_length=200)
#     is_available = models.BooleanField(default=True)
#     created = models.DateTimeField(default=datetime.now, blank=True)

#     def __str__(self):
#         return str(self.name)

#     class Meta:
#         ordering = ('-created',)
#         index_together = (('id', 'slug'),)

#     def get_absolute_url(self):
#         return reverse('user:product_detail', args=[self.id, self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    url_flipkart = models.URLField(blank=True,null=True)
    url_amazon = models.URLField(blank=True,null=True)

    price_flipkart_xmlpath = models.CharField(max_length=1000,blank=True,null=True)
    price_amazon_xmlpath = models.CharField(max_length=1000,blank=True,null=True)

    comapare_flipkart_price=models.CharField(blank=True,null=True,max_length=20)
    compare_amazon_price=models.CharField(blank=True,null=True,max_length=20)

    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)
    count=models.IntegerField(null=True,blank=True,default=0)
    # make all thumbnails at most 140x140pixels

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class ProductAdd(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    comapare=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    flipkart_image=models.ImageField(upload_to='flipkart',default='default-product.png', blank=True)
    amazone_image=models.ImageField(upload_to='amazone',default='default-product.png', blank=True)
    comapare_flipkart_price=models.FloatField(blank=True,null=True)
    compare_amazon_price=models.FloatField(blank=True,null=True)
    slug = models.SlugField(max_length=50, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    description=models.TextField(blank=True,null=True)
    is_available=models.BooleanField(default=True)

    our_product_image=models.ImageField(upload_to='our_product')
    our_price=models.IntegerField(blank=True,null=True)
    count=models.FloatField(null=True,blank=True,default=0)
    
    
    class Meta:
       ordering = ('-created_on',)
       index_together = (('id', 'slug'),)
    
    def get_absolute_url(self):
        return reverse('user:product_detail', args=[self.id, self.slug])

   
    def __str__(self):
        return str(self.name)





class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(ProductAdd,on_delete=models.CASCADE,null=True,blank=True)
    review=models.TextField()
    count=models.IntegerField()
    def __str__(self):
        return str(self.user.username)




class Report(models.Model):
    product=models.ForeignKey(ProductAdd,on_delete=models.CASCADE,null=True,blank=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.product)



