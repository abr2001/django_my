from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Country, Wine
from main.serializers import CountrySerializer, WineSerializer


class WineListAPIView(generics.ListAPIView):
    """
    API endpoint для получения списка вин.
    Поддерживает фильтрацию по типу вина и стране.
    
    Query параметры:
    - wine_type: red, white, rose, sparkling
    - country: ID страны
    - in_stock: true/false
    """
    queryset = Wine.objects.select_related('country').all()
    serializer_class = WineSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        wine_type = self.request.query_params.get('wine_type')
        if wine_type:
            queryset = queryset.filter(wine_type=wine_type)
        
        country_id = self.request.query_params.get('country')
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock is not None:
            in_stock_bool = in_stock.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(in_stock=in_stock_bool)
        
        return queryset

class WineDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint для получения детальной информации о вине.
    """
    queryset = Wine.objects.select_related('country').all()
    serializer_class = WineSerializer

class CountryListAPIView(generics.ListAPIView):
    """
    API endpoint для получения списка стран.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CatalogStatsAPIView(APIView):
    """
    API endpoint для получения статистики каталога.
    """
    def get(self, request):
        total_wines = Wine.objects.count()
        in_stock_wines = Wine.objects.filter(in_stock=True).count()
        
        wines_by_type = {}
        for wine_type, display_name in Wine.WINE_TYPES:
            count = Wine.objects.filter(wine_type=wine_type, in_stock=True).count()
            wines_by_type[wine_type] = {
                'name': display_name,
                'count': count
            }
        
        countries_count = Country.objects.count()
        
        return Response({
            'total_wines': total_wines,
            'in_stock_wines': in_stock_wines,
            'out_of_stock_wines': total_wines - in_stock_wines,
            'wines_by_type': wines_by_type,
            'countries_count': countries_count,
        })
