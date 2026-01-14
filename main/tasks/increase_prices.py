import logging
from decimal import Decimal

from django.utils import timezone
from celery import shared_task

from main.models import Wine

logger = logging.getLogger(__name__)


@shared_task
def increase_prices():
    """
    Фоновая задача для повышения цен на все вина на 10%.
    Запускается автоматически 1-го числа каждого месяца в 00:00.
    """
    try:
        wines = Wine.objects.all()
        updated_count = 0
        
        for wine in wines:
            old_price = wine.price
            wine.price = wine.price * Decimal('1.10')
            wine.save()
            updated_count += 1
            
            logger.info(
                f"Цена вина '{wine.name}' повышена с {old_price} ₽ до {wine.price} ₽"
            )
        
        logger.info(
            f"Задача завершена. Обновлено цен: {updated_count}. "
            f"Время выполнения: {timezone.now()}"
        )
        
        return {
            'status': 'success',
            'updated_count': updated_count,
            'timestamp': str(timezone.now())
        }
        
    except Exception as e:
        logger.error(f"Ошибка при повышении цен: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': str(timezone.now())
        }
