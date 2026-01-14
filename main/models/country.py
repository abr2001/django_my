from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    code = models.CharField(max_length=3, unique=True, verbose_name='Код страны')
    
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']
    
    def __str__(self):
        return self.name
