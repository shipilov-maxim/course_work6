from django.db import models
from distribution.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='preview/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания')
    views_count = models.PositiveIntegerField(verbose_name='Просмотры', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
