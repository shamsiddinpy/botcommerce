from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from users.models import User, Person, ShopUser, Plan, PlanPricing, Quotas, PlanQuotas, PlanInvoice


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, CustomUserAdmin)


@admin.register(ShopUser)
class ShopUserAdmin(ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'type')
    search_fields = ('email', 'first_name', 'last_name')
    # list_filter = ('is_staff', 'is_superuser', 'is_active')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(PlanPricing)
class PlanPricingAdmin(admin.ModelAdmin):
    list_display = ('name', 'period')


@admin.register(Quotas)
class QuotasAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(PlanQuotas)
class PlanQuotasAdmin(admin.ModelAdmin):
    list_display = ('value',)


@admin.register(PlanInvoice)
class PlanInvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')
