# Generated by Django 3.2.8 on 2021-11-05 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart1', '0002_cartitem_price1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]