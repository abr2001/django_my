from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
]
