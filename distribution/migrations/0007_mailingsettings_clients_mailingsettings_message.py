# Generated by Django 4.2.11 on 2024-04-09 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0006_alter_client_comment_alter_client_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingsettings',
            name='clients',
            field=models.ManyToManyField(to='distribution.client', verbose_name='Клиенты рассылки'),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='distribution.message', verbose_name='Сообщение'),
        ),
    ]
