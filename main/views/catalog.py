from django.views.generic import ListView

from main.models import Wine


class CatalogView(ListView):
    model = Wine
    template_name = 'main/catalog.html'
    context_object_name = 'wines'
    
    def get_queryset(self):
        queryset = Wine.objects.select_related('country').filter(in_stock=True)
        wine_type = self.request.GET.get('type')
        
        if wine_type:
            queryset = queryset.filter(wine_type=wine_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_type'] = self.request.GET.get('type')
        return context
