# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from product.models import *


# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'wishlist of {}'.format(self.user.username)


class WishlistItem(models.Model):

    wishlist = models.ForeignKey(
        Wishlist,
        related_name='wishlist_items',
        null=True,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(ProductAdd, related_name='wishlist_item',
    on_delete=models.CASCADE,
    
    )

    def __str__(self):
        return '{}'.format(self.product.name)
