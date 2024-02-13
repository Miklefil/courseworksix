from django.db import models
from django.utils import timezone

import users.models

NULLABLE = {'null': True, 'blank': True}

STATUS_CHOICES = [
    ('start', 'start'),
    ('finish', 'finish'),
    ('created', 'created'),
]
INTERVAL_CHOICES = [
    ('once_a_day', 'once_a_day'),
    ('once_a_week', 'once_a_week'),
    ('once_a_month', 'once_a_month'),
]


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='чей клиент')

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    def __repr__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='тема')
    content = models.TextField(verbose_name='содержание')
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mail(models.Model):
    name = models.CharField(verbose_name="название", max_length=50)
    client = models.ManyToManyField(Client, verbose_name="кому")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение", **NULLABLE)
    start_date = models.DateTimeField(default=timezone.now, verbose_name="начало")
    next_date = models.DateTimeField(default=timezone.now, verbose_name="следующее")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="конец")
    interval = models.CharField(default="разовая", max_length=50, verbose_name="интервал", choices=INTERVAL_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="статус")
    is_active = models.BooleanField(default=True, verbose_name="действующая")
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, verbose_name="владелец рассылки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('start_date',)
        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='время последней рассылки')
    status = models.CharField(max_length=50, verbose_name='статус попытки', null=True)
    response = models.CharField(max_length=200, verbose_name="ответ почтового сервера", **NULLABLE)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.last_mail_time = None

    def __str__(self):
        return f'Отправлено: {self.last_mailing_time}, ' \
               f'Статус: {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'


# Create your models here.
