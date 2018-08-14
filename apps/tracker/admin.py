from django.contrib import admin

from . import models


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


class TrackPointInline(admin.TabularInline):
    model = models.TrackPoint
    extra = 0
    fields = ('timestamp', 'price')
    readonly_fields = fields


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'last_price', 'price_drop_short', 'price_drop_long')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('property', 'identifier', 'url')

    inlines = (TrackPointInline,)
