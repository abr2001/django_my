from django.urls import path

from main.views import (
    CatalogStatsAPIView,
    CountryListAPIView,
    CountrySalesAnalyticsView,
    DailySalesAnalyticsView,
    HourlySalesView,
    SalesMetricsView,
    TopWinesAnalyticsView,
    WineDetailAPIView,
    WineListAPIView,
)

app_name = 'api'

urlpatterns = [
    path('wines/', WineListAPIView.as_view(), name='wine-list'),
    path('wines/<int:pk>/', WineDetailAPIView.as_view(), name='wine-detail'),
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
    path('stats/', CatalogStatsAPIView.as_view(), name='catalog-stats'),
    
    # Analytics endpoints
    path('analytics/daily-sales/', DailySalesAnalyticsView.as_view(), name='daily-sales'),
    path('analytics/country-sales/', CountrySalesAnalyticsView.as_view(), name='country-sales'),
    path('analytics/top-wines/', TopWinesAnalyticsView.as_view(), name='top-wines'),
    path('analytics/metrics/', SalesMetricsView.as_view(), name='sales-metrics'),
    path('analytics/hourly-sales/', HourlySalesView.as_view(), name='hourly-sales'),
]
