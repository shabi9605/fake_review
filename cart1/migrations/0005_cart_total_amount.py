# Generated by Django 3.2.8 on 2021-11-05 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart1', '0004_cartitem_price2'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
