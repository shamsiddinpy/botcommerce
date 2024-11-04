# Generated by Django 5.0.7 on 2024-10-30 07:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0003_initial'),
        ('shops', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shop',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view', to='users.plan'),
        ),
        migrations.AddField(
            model_name='shop',
            name='services',
            field=models.ManyToManyField(through='orders.ShopService', to='orders.service'),
        ),
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories_set', to='shops.shop'),
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shopcategory', verbose_name='Kategoriyalar'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight_class',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='weights', to='shops.weight', verbose_name='Vazn birligi'),
        ),
        migrations.AddField(
            model_name='attributevariant',
            name='weight_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='shops.weight'),
        ),
    ]
