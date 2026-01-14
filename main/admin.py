from django.contrib import admin

from .models import Country, Wine


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ['name', 'wine_type', 'country', 'year', 'price', 'in_stock']
    list_filter = ['wine_type', 'country', 'in_stock']
    search_fields = ['name', 'country__name', 'region', 'grape_variety']
    list_editable = ['in_stock']
