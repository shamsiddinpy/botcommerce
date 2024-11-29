# Generated by Django 5.0.7 on 2024-11-28 11:38

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import users.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='mijozning ismi')),
                ('phone', models.CharField(max_length=100, verbose_name='mijozning telfoni raqmi')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=150)),
                ('code', models.CharField(max_length=100, verbose_name='qaysi tarfidan foydalanyotgani')),
            ],
        ),
        migrations.CreateModel(
            name='Quotas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Kvotalar Nome')),
                ('description', models.TextField(verbose_name='Kvotalar Tavsif')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('type', models.CharField(choices=[('email', 'Email'), ('telegram', 'Telegram'), ('facebook', 'Facebook')], max_length=255)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator], verbose_name='foydalanuvchini nomi')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('public_offer', models.BooleanField(default=False)),
                ('invitation_code', models.CharField(max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('default_shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.language')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PlanInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.CharField(max_length=55, verbose_name='Narxi')),
                ('payed_at', models.DateTimeField(blank=True, null=True, verbose_name='da toʻlangan')),
                ('pay_url', models.URLField(blank=True, null=True, verbose_name='tolov url')),
                ('plan_extended_from', models.DateField()),
                ('plan_extended_until', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('completed', 'Completed')], db_default='new', max_length=25)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_invoices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlanPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('period_type', models.IntegerField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], verbose_name='Davr turi')),
                ('price', models.PositiveIntegerField(verbose_name='Narxi')),
                ('original_price', models.PositiveIntegerField(verbose_name='Haqiqiy narxi')),
                ('period', models.IntegerField(verbose_name='davr')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='shops.currency')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlanQuotas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, verbose_name='Qiymat')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plan')),
                ('quotas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.quotas')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='quotas',
            field=models.ManyToManyField(blank=True, through='users.PlanQuotas', to='users.quotas'),
        ),
        migrations.CreateModel(
            name='ShopUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator])),
                ('type', models.CharField(max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('is_blocked', models.BooleanField(db_default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.language')),
                ('person', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.person')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='shops.shop')),
            ],
            options={
                'unique_together': {('username', 'shop')},
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
