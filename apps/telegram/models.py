from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import CASCADE, Model, TextChoices


class TelegramChannel(Model):  # ✅
    chat = models.CharField(max_length=255, verbose_name='Telegram kanal username')
    shop = models.ForeignKey('shops.Shop', CASCADE, related_name='channels')

    class Meta:
        verbose_name = 'Telegram kanal'
        verbose_name_plural = 'Telegram kanallar'
        unique_together = [
            ('shop', 'chat')
        ]

    def __str__(self):
        return f"{self.chat}"


class ChannelMessage(Model):  # ✅
    class FileType(TextChoices):
        TEXT = 'text', 'Text'
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Video'

    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = models.CharField(max_length=4100)
    chat = models.ForeignKey('telegram.TelegramChannel', CASCADE, related_name='messages')
    is_scheduled = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    file_type = models.CharField(max_length=20, choices=FileType.choices, db_default=FileType.TEXT)
    status = models.CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                              db_default=MessageStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Xabar yaratilgan vaqti')

    class Meta:
        verbose_name = 'Telegram Kanal xabari'
        verbose_name_plural = 'Telegram kanal xabarlari'

    def __str__(self):
        return f"{self.id}. Message of {self.chat}"


class ChatMessage(Model):  # ✅
    class Type(TextChoices):
        USER = 'user', 'User'
        OWNER = 'owner', 'Owner'

    class ContentType(TextChoices):
        TEXT = 'text', 'Text'

    message = models.CharField('Xabar', max_length=4100)
    chat_user = models.ForeignKey('users.ShopUser', CASCADE, related_name='messages')
    content_type = models.CharField(max_length=10, choices=Type.choices)
    seen = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')


class BroadCastMessage(Model):  # ✅
    class MessageStatus(TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = models.CharField(max_length=4100, verbose_name='Xabar')
    shop = models.ForeignKey('shops.Shop', CASCADE)
    is_scheduled = models.BooleanField(default=False)
    lat = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lat")
    lon = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lon")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    received_users = models.IntegerField(default=0, verbose_name='Qabul qiluvchilar soni')
    status = models.CharField('Xabarning statusi', max_length=20, choices=MessageStatus.choices,
                              db_default=MessageStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')
    attachments = GenericRelation('shops.Attachment', 'record_id', blank=True)

    class Meta:
        verbose_name = 'Axborotnoma'
        verbose_name_plural = 'Axborotnomalar'


class Commerce(Model):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = models.CharField(max_length=30, verbose_name='Domen Nomi')
    status = models.CharField(max_length=8, choices=Status.choices, verbose_name='Sayt aktiv yoki  aktivmasligi')
    template_color = models.ForeignKey('shops.TemplateColor', CASCADE, related_name='sites')
    is_configured = models.BooleanField(db_default=True)
    is_sub_domain = models.BooleanField(db_default=True, verbose_name='Sayt domen quygan yoki yuqligi')
    shop = models.OneToOneField('shops.Shop', CASCADE, related_name='sites')


class TelegramBot(Model):  # ✅
    username = models.CharField(max_length=255, unique=True, verbose_name='Telegram username')
    token = models.CharField(max_length=255, unique=True, verbose_name='BotFather dan olingan token')
    group_access_token = models.CharField(max_length=255, unique=True, verbose_name='guruhda ishlashi uchun token')
    is_new_template = models.BooleanField(verbose_name='web app True odiiy bot False')
    order_button_url = models.CharField(max_length=255)
    shop = models.OneToOneField('shops.Shop', CASCADE, related_name='telegram_bots')
