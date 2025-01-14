from django.contrib import admin
from .models import RealEstate, RealEstateLiked
from .models import *


class BankImageStackedInline(admin.StackedInline):
    extra = 1
    model = BankImage
    readonly_fields = ("created_at", "updated_at")


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "area", "bedrooms", "bathrooms", "has_pool", "has_garden", "is_available")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Informations",
            {
                "classes": ["wide", "collapse"],
                "fields": (
                    "title",
                    "description",
                    "address",
                    "city",
                    "price",
                    "real_estate_type",
                    "area",
                    "bedrooms",
                    "bathrooms",
                    "has_pool",
                    "has_garden",
                    "is_available",
                ),
            },
        ),
        (
            "Images",
            {
                "classes": ["wide", "collapse"],
                "fields": ("image_first", "image_second"),
            },
        ),
    )

    inlines = [BankImageStackedInline]


@admin.register(BankImage)
class BankImageAdmin(admin.ModelAdmin):
    fields = ["__all__"]
    readonly_fields = ("created_at", "updated_at")


@admin.register(RealEstateLiked)
class RealEstateLikedAdmin(admin.ModelAdmin):
    fields = ["user", "real_estate"]
    readonly_fields = ("created_at", "updated_at")