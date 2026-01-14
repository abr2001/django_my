import logging
import random
from datetime import datetime, timedelta

from celery import shared_task

from main.clickhouse_client import clickhouse_client
from main.models import Wine

logger = logging.getLogger(__name__)


@shared_task
def sync_wines_to_clickhouse():
    """
    Синхронизация данных о винах из PostgreSQL в ClickHouse.
    Запускается периодически для обновления справочника вин.
    """
    sync_start = datetime.now()
    
    try:
        wines = Wine.objects.select_related('country').all()
        
        wines_data = []
        for wine in wines:
            wines_data.append([
                wine.id,
                wine.name,
                wine.wine_type,
                wine.country.id if wine.country else 0,
                wine.country.name if wine.country else 'Unknown',
                wine.region,
                wine.year,
                float(wine.price),
                wine.volume,
                float(wine.alcohol),
                wine.grape_variety,
                wine.created_at
            ])
        
        records_synced = clickhouse_client.insert_wines(wines_data)
        clickhouse_client.log_sync('wines', records_synced, sync_start, 'success')
        
        logger.info(f"Синхронизировано {records_synced} вин в ClickHouse")
        
        return {
            'status': 'success',
            'records_synced': records_synced,
            'timestamp': str(datetime.now())
        }
        
    except Exception as e:
        logger.error(f"Ошибка синхронизации вин: {str(e)}")
        clickhouse_client.log_sync('wines', 0, sync_start, 'error', str(e))
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': str(datetime.now())
        }


@shared_task
def generate_sample_sales_data(num_sales=100):
    """
    Генерация тестовых данных о продажах для демонстрации аналитики.
    В реальном проекте эти данные будут поступать из модели Order.
    """
    sync_start = datetime.now()
    
    try:
        wines = Wine.objects.select_related('country').all()
        if not wines:
            return {'status': 'error', 'error': 'No wines found'}
        
        sales_data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(num_sales):
            wine = random.choice(wines)
            quantity = random.randint(1, 5)
            sale_date = base_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23)
            )
            
            sales_data.append([
                i + 1,  # sale_id
                wine.id,
                wine.name,
                wine.wine_type,
                wine.country.name if wine.country else 'Unknown',
                quantity,
                float(wine.price),
                float(wine.price * quantity),
                sale_date,
                sale_date.year,
                sale_date.month,
                sale_date.day,
                sale_date.hour,
                sale_date.weekday()
            ])
        
        records_synced = clickhouse_client.insert_sales(sales_data)
        clickhouse_client.log_sync('sales', records_synced, sync_start, 'success')
        
        logger.info(f"Сгенерировано {records_synced} тестовых продаж")
        
        return {
            'status': 'success',
            'records_synced': records_synced,
            'timestamp': str(datetime.now())
        }
        
    except Exception as e:
        logger.error(f"Ошибка генерации данных о продажах: {str(e)}")
        clickhouse_client.log_sync('sales', 0, sync_start, 'error', str(e))
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': str(datetime.now())
        }
