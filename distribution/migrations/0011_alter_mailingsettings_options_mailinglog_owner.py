# Generated by Django 4.2.11 on 2024-04-14 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distribution', '0010_remove_mailinglog_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingsettings',
            options={'verbose_name': 'Настройки рассылки', 'verbose_name_plural': 'Настройки рассылки'},
        ),
        migrations.AddField(
            model_name='mailinglog',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
