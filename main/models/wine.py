from django.db import models

from .country import Country


class Wine(models.Model):
    WINE_TYPES = [
        ('red', 'Красное'),
        ('white', 'Белое'),
        ('rose', 'Розовое'),
        ('sparkling', 'Игристое'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    wine_type = models.CharField(max_length=20, choices=WINE_TYPES, verbose_name='Тип вина')
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='wines',
        verbose_name='Страна',
        null=True,
    )
    region = models.CharField(max_length=100, verbose_name='Регион')
    year = models.IntegerField(verbose_name='Год')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    volume = models.IntegerField(default=750, verbose_name='Объем (мл)')
    alcohol = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Крепость (%)')
    description = models.TextField(verbose_name='Описание')
    grape_variety = models.CharField(max_length=200, verbose_name='Сорт винограда')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Вино'
        verbose_name_plural = 'Вина'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.year})"
