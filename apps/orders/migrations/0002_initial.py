# Generated by Django 5.0.7 on 2024-08-19 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to='shops.currency'),
        ),
    ]
