# Generated by Django 5.0.7 on 2024-11-28 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0002_initial'),
        ('telegram', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='chat_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='users.shopuser'),
        ),
        migrations.AddField(
            model_name='commerce',
            name='shop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='shops.shop'),
        ),
        migrations.AddField(
            model_name='commerce',
            name='template_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='shops.templatecolor'),
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='shop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='telegram_bots', to='shops.shop'),
        ),
        migrations.AddField(
            model_name='telegramchannel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='shops.shop'),
        ),
        migrations.AddField(
            model_name='channelmessage',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='telegram.telegramchannel'),
        ),
        migrations.AlterUniqueTogether(
            name='telegramchannel',
            unique_together={('shop', 'chat')},
        ),
    ]
