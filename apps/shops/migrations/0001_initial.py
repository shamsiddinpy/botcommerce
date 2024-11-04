# Generated by Django 5.0.7 on 2024-10-30 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='atribut nomi')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='davlatlar nomi')),
                ('code', models.CharField(max_length=255, verbose_name='davlatlar kodi')),
            ],
            options={
                'verbose_name': 'Davlat',
                'verbose_name_plural': 'Davlatlar',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nomi')),
                ('order', models.PositiveSmallIntegerField(db_default=1, default=1, verbose_name='rangi')),
            ],
            options={
                'verbose_name': 'Pul birlgi',
                'verbose_name_plural': 'Pul birlklari',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nomi')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('icon', models.CharField(blank=True, max_length=255, verbose_name='Bayrog rasmi')),
            ],
            options={
                'verbose_name': 'Davlat tili',
                'verbose_name_plural': 'Davlat tilari',
            },
        ),
        migrations.CreateModel(
            name='Length',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': "Do'kon toifasi",
                'verbose_name_plural': "Do'kon toifalari",
            },
        ),
        migrations.CreateModel(
            name='TemplateColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Nomi')),
                ('color', models.CharField(max_length=55, verbose_name='Rangi')),
            ],
            options={
                'verbose_name': 'Shablon rangi',
                'verbose_name_plural': 'Shablon ranglari',
            },
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('record_id', models.PositiveIntegerField()),
                ('key', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='atribut qiymati')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='shops.attribute', verbose_name='atribut')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('emoji', models.CharField(blank=True, max_length=255, null=True)),
                ('show_in_ecommerce', models.BooleanField(db_default=False, verbose_name="Web saytda ko'rsatish")),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.IntegerField(default=1, verbose_name='tartiblash tartibi')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shops.category')),
            ],
            options={
                'verbose_name': 'Kategorya',
                'verbose_name_plural': 'Kategorylar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Mahsulotning nomi')),
                ('full_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Mahsulotning umumiy narxi')),
                ('purchase_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mahsulotning sotib olish narxi')),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Mahsulot soni')),
                ('ikpu_code', models.IntegerField(blank=True, null=True, verbose_name='Mahsulotning IKPU kodi')),
                ('packing_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mahsulotning qadoqlash kodi')),
                ('has_available', models.BooleanField(default=True, verbose_name="Mahsulotning o'ya sah")),
                ('package_code', models.IntegerField(blank=True, null=True, verbose_name='qadoq ko`di')),
                ('stock_status', models.CharField(choices=[('indefinite', 'Indefinite'), ('fixed', 'Fixed'), ('not available', 'Not available')], max_length=100)),
                ('unit', models.CharField(choices=[('item', 'Item'), ('weight', 'Weight')], max_length=20, verbose_name='Birligi')),
                ('barcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mahsulotning shtrix kodi')),
                ('vat_percent', models.IntegerField(blank=True, null=True, verbose_name='QQS foizi')),
                ('position', models.IntegerField(db_default=1, verbose_name='sort order')),
                ('length', models.IntegerField(blank=True, verbose_name='Mahsulotning uzunligi')),
                ('width', models.IntegerField(blank=True, verbose_name='Mahsulotning kengligi')),
                ('height', models.IntegerField(blank=True, verbose_name='Mahsulotning balandligi')),
                ('weight', models.IntegerField(blank=True, verbose_name='Mahsulotning vazni')),
                ('internal_notes', models.TextField(blank=True, verbose_name='Ichki eslatmalar')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shops.category', verbose_name='Kategoriya')),
                ('length_class', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='lengths', to='shops.length', verbose_name='Uzunlik birligi')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttributeVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Sotuv narxi')),
                ('full_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Umumiy narxi')),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('package_code', models.IntegerField(blank=True, null=True)),
                ('ikpu_code', models.IntegerField(blank=True, null=True)),
                ('stock_status', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(max_length=20)),
                ('barcode', models.IntegerField(blank=True, null=True)),
                ('has_available', models.BooleanField(db_default=False)),
                ('vat_percent', models.IntegerField(db_default=0)),
                ('length_class_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='shops.length')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shops.product')),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='shops.product', verbose_name='mahsulotlar'),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=55, verbose_name="Do'kon nomi")),
                ('phone', models.CharField(max_length=50, verbose_name='Biznes telefon raqami')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Telefon raqami')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], db_default='active', max_length=8)),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='Location lat')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='Location lon')),
                ('starts_at', models.TimeField(blank=True, null=True, verbose_name='Dan')),
                ('ends_at', models.TimeField(blank=True, null=True, verbose_name='Gacha')),
                ('has_terminal', models.BooleanField(db_default=True)),
                ('about_us', models.TextField(blank=True, null=True, verbose_name='Biz haqimizda')),
                ('facebook', models.URLField(blank=True, max_length=255, null=True, verbose_name='Facebook')),
                ('instagram', models.URLField(blank=True, max_length=255, null=True, verbose_name='Instagram')),
                ('telegram', models.URLField(blank=True, max_length=255, null=True, verbose_name='Telegram')),
                ('email', models.URLField(blank=True, max_length=255, null=True, verbose_name='Elektron pochta')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Manzil')),
                ('is_new_products_show', models.BooleanField(db_default=False, default=False, verbose_name="'Yangi mahsulotlar' sahifasini ko'rsatish")),
                ('is_popular_products_show', models.BooleanField(db_default=False, default=False, verbose_name="Ommabop mahsulotlar' sahifasini ko'rsatish")),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.country', verbose_name="Ro'yxatdan o'tgan davlat")),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.currency', verbose_name='Pul birligi')),
                ('languages', models.ManyToManyField(blank=True, to='shops.language', verbose_name='Til')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
