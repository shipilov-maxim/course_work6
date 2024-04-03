from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    surname = models.CharField(max_length=64, verbose_name='Фамилия', **NULLABLE)
    name = models.CharField(max_length=64, verbose_name='Имя', **NULLABLE)
    patronymic = models.CharField(max_length=64, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(default=None, verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Письмо')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    start_time = models.DateTimeField(verbose_name='Дата начала рассылки')
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус рассылки')
