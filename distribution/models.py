from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    surname = models.CharField(max_length=64, verbose_name='Фамилия', **NULLABLE)
    name = models.CharField(max_length=64, verbose_name='Имя', **NULLABLE)
    patronymic = models.CharField(max_length=64, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Письмо')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

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
    end_time = models.DateTimeField(verbose_name='Дата конца рассылки')
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Статус работы')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=None, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.message} {self.periodicity}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'Настройки рассылки'
        permissions = [
            ('set_active', 'Can active mailingsettings')
        ]


class MailingLog(models.Model):
    time = models.DateTimeField(verbose_name='Дата и время создания лога', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус попытки')
    server_response = models.CharField(max_length=1000, verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
