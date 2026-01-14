import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def test_task():
    """
    Тестовая задача для проверки работы Celery.
    """
    logger.info("Тестовая задача выполнена успешно!")
    return "Test task completed"
