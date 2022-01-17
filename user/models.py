from django.db import models
from django.contrib.auth.models import User
# Create your models
class Contacts(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=300)
    message=models.TextField()

    def __str__(self):
        return str(self.name)

class Register(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images',default='default.jpg')

    customer='customer'
    manager='manager'

    user_types=[
        (customer,customer),
        (manager,manager)
    ]

    user_type=models.CharField(max_length=30,choices=user_types,default=customer)

    def __str__(self):
        return str(self.user.username)
