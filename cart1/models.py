from django.db import models
from product.models import ProductAdd
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    # paid = models.BooleanField(default=False)
    # is_in_order = models.BooleanField(default=False)
    total_amount=models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'cart {}'.format(self.user.username)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost1(self):
        return sum(item.get_cost1() for item in self.items.all())

    def get_total_cost2(self):
        return sum(item.get_cost2() for item in self.items.all())

    
    def save(self,*args,**kwargs):
        self.total_amount=sum(item.get_cost2() for item in self.items.all())
        print(self.total_amount)
        super().save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
    null=True,
    on_delete=models.CASCADE,
    )
    product = models.ForeignKey(ProductAdd,
    related_name='cart_items',
    on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.product)

    def get_cost(self):
        return self.price * self.quantity

    def get_cost1(self):
        return self.price1 * self.quantity

    def get_cost2(self):
        return self.price2 * self.quantity
    

 

