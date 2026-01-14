from rest_framework import serializers

from main.models import Wine

from .country import CountrySerializer


class WineSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    wine_type_display = serializers.CharField(source='get_wine_type_display', read_only=True)
    
    class Meta:
        model = Wine
        fields = [
            'id',
            'name',
            'wine_type',
            'wine_type_display',
            'country',
            'region',
            'year',
            'price',
            'volume',
            'alcohol',
            'description',
            'grape_variety',
            'in_stock',
            'created_at',
        ]
