# Generated by Django 3.2.8 on 2021-10-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]