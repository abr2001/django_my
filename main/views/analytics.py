import logging
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.clickhouse_client import clickhouse_client

logger = logging.getLogger(__name__)

class DailySalesAnalyticsView(APIView):
    """
    API endpoint для получения статистики продаж по дням.
    
    Query параметры:
    - start_date: дата начала (YYYY-MM-DD)
    - end_date: дата окончания (YYYY-MM-DD)
    """
    
    def get(self, request):
        try:
            end_date = request.query_params.get('end_date', datetime.now().date())
            start_date = request.query_params.get('start_date', 
                                                  (datetime.now() - timedelta(days=30)).date())
            
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            results = clickhouse_client.get_daily_sales(start_date, end_date)
            
            data = []
            for row in results:
                data.append({
                    'date': str(row[0]),
                    'wine_type': row[1],
                    'quantity': row[2],
                    'revenue': float(row[3]),
                    'orders': row[4],
                    'avg_price': float(row[5])
                })
            
            return Response({
                'start_date': str(start_date),
                'end_date': str(end_date),
                'data': data
            })
            
        except Exception as e:
            logger.error(f"Error in DailySalesAnalyticsView: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CountrySalesAnalyticsView(APIView):
    """
    API endpoint для получения статистики продаж по странам.
    
    Query параметры:
    - start_date: дата начала (YYYY-MM-DD)
    - end_date: дата окончания (YYYY-MM-DD)
    """
    
    def get(self, request):
        try:
            end_date = request.query_params.get('end_date', datetime.now().date())
            start_date = request.query_params.get('start_date',
                                                  (datetime.now() - timedelta(days=30)).date())
            
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            results = clickhouse_client.get_country_sales(start_date, end_date)
            
            data = []
            for row in results:
                data.append({
                    'country': row[0],
                    'quantity': row[1],
                    'revenue': float(row[2]),
                    'orders': row[3]
                })
            
            return Response({
                'start_date': str(start_date),
                'end_date': str(end_date),
                'data': data
            })
            
        except Exception as e:
            logger.error(f"Error in CountrySalesAnalyticsView: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TopWinesAnalyticsView(APIView):
    """
    API endpoint для получения топ продаваемых вин.
    
    Query параметры:
    - limit: количество вин (по умолчанию 10)
    - start_date: дата начала (YYYY-MM-DD, опционально)
    - end_date: дата окончания (YYYY-MM-DD, опционально)
    """
    
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            results = clickhouse_client.get_top_wines(limit, start_date, end_date)
            
            data = []
            for row in results:
                data.append({
                    'wine_name': row[0],
                    'wine_type': row[1],
                    'country': row[2],
                    'total_quantity': row[3],
                    'total_revenue': float(row[4]),
                    'order_count': row[5],
                    'avg_price': float(row[6])
                })
            
            return Response({
                'limit': limit,
                'start_date': str(start_date) if start_date else None,
                'end_date': str(end_date) if end_date else None,
                'data': data
            })
            
        except Exception as e:
            logger.error(f"Error in TopWinesAnalyticsView: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SalesMetricsView(APIView):
    """
    API endpoint для получения общих метрик продаж.
    
    Query параметры:
    - start_date: дата начала (YYYY-MM-DD)
    - end_date: дата окончания (YYYY-MM-DD)
    """
    
    def get(self, request):
        try:
            end_date = request.query_params.get('end_date', datetime.now().date())
            start_date = request.query_params.get('start_date',
                                                  (datetime.now() - timedelta(days=30)).date())
            
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
            metrics = clickhouse_client.get_sales_metrics(start_date, end_date)
            
            if metrics:
                return Response({
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'metrics': {
                        'total_orders': metrics[0],
                        'total_revenue': float(metrics[1]),
                        'avg_order_value': float(metrics[2]),
                        'total_items_sold': metrics[3],
                        'unique_wines_sold': metrics[4]
                    }
                })
            else:
                return Response({
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'metrics': None,
                    'message': 'No data available for the specified period'
                })
            
        except Exception as e:
            logger.error(f"Error in SalesMetricsView: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HourlySalesView(APIView):
    """
    API endpoint для получения статистики продаж по часам.
    
    Query параметры:
    - date: дата (YYYY-MM-DD)
    """
    
    def get(self, request):
        try:
            date_str = request.query_params.get('date', str(datetime.now().date()))
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            results = clickhouse_client.get_hourly_sales(date)
            
            data = []
            for row in results:
                data.append({
                    'hour': row[0],
                    'orders': row[1],
                    'revenue': float(row[2]),
                    'items_sold': row[3]
                })
            
            return Response({
                'date': str(date),
                'data': data
            })
            
        except Exception as e:
            logger.error(f"Error in HourlySalesView: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
