# Generated by Django 5.0.7 on 2024-10-30 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_initial'),
        ('shops', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='users.person'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.shopuser'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.currency'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_code', to='shops.attributevariant'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop', verbose_name="Do'kon"),
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.promocode'),
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('code', 'type')},
        ),
        migrations.AddField(
            model_name='field',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='orders.service'),
        ),
        migrations.AddField(
            model_name='shopservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.service'),
        ),
        migrations.AddField(
            model_name='shopservice',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.shopservice'),
        ),
        migrations.AddField(
            model_name='shopservicefield',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.field'),
        ),
        migrations.AddField(
            model_name='shopservicefield',
            name='shop_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.shopservice'),
        ),
        migrations.AddField(
            model_name='shopservice',
            name='fields',
            field=models.ManyToManyField(through='orders.ShopServiceField', to='orders.field'),
        ),
        migrations.AlterUniqueTogether(
            name='promocode',
            unique_together={('shop', 'code')},
        ),
    ]
