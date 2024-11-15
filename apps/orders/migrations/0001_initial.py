# Generated by Django 5.0.7 on 2024-11-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('max_length', models.IntegerField()),
                ('required', models.BooleanField()),
                ('type', models.CharField(choices=[('integer', 'Integer'), ('string', 'String'), ('text', 'Text'), ('list', 'List'), ('video', 'Video'), ('image', 'Image'), ('geolocation', 'Geolocation')], max_length=255)),
                ('provider_labels', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='yetkazib berish sanasi')),
                ('delivery_type', models.CharField(choices=[('take away', 'Take away'), ('delivery', 'Delivery'), ('online delivery', 'Online Delivery')], max_length=20)),
                ('delivery_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='yetkazib berish narxi ')),
                ('is_archived', models.BooleanField(default=False, verbose_name='arxivdagi zakaslar')),
                ('note', models.TextField(blank=True, null=True, verbose_name='usering fikri')),
                ('order_type', models.CharField(choices=[('telegram', 'Telegram'), ('web', 'Web'), ('whatsapp', 'Whatsapp')], max_length=20)),
                ('paid', models.BooleanField(db_default=False, verbose_name="To'lov qilingan yoki yo'qligi")),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('confirmed', 'Confirmed'), ('in_progress', 'In_progres'), ('successfully', 'Successfully'), ('Canceled', 'Canceled'), ('payment cancelled', 'Payment Cancelled'), ('returned', 'Returned')], max_length=20)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='umumiy narxi')),
                ('door_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='domni nomiri')),
                ('floor_number', models.IntegerField(blank=True, null=True, verbose_name='Qavat raqami')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='manzil')),
                ('apartment_number', models.IntegerField(blank=True, null=True, verbose_name='kvartera raqami')),
                ('lon', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(db_default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('free_delivery', 'Free_delivery'), ('discount', 'Discount')], max_length=20, verbose_name='Promo kodi turi')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Foydalanish miqdori')),
                ('percent', models.IntegerField(default=0, verbose_name='Chegirma foizi')),
                ('limit', models.IntegerField(verbose_name='promode cheklash vaqti')),
                ('starts_at', models.DateField(verbose_name=' promocde boshlash vaqti')),
                ('ends_at', models.DateField(verbose_name='promo code tugash vaqti ')),
                ('is_active', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Promo kod',
                'verbose_name_plural': 'Promo kodlar',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('delivery', 'Delivery'), ('payment', 'Payment')], max_length=15)),
                ('title', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('internal', 'Internal'), ('inplace', 'Inplace'), ('telegram', 'Telegram'), ('web', 'Web'), ('instalment', 'Instalment')], max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('not_exists', 'Not exists')], db_default='inactive', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ShopServiceField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.JSONField(default=dict)),
            ],
        ),
    ]