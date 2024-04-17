import calendar
import logging
import random
from datetime import datetime, timedelta
from smtplib import SMTPException

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.utils import timezone
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from blog.models import Blog
from config import settings
from config.settings import CACHE_ENABLED
from distribution.models import MailingLog, MailingSettings, Client

logger = logging.getLogger(__name__)

today = datetime.today()
PERIODICITY = {
    "Раз в день": timedelta(days=1),
    "Раз в неделю": timedelta(weeks=1),
    "Раз в месяц": timedelta(days=calendar.monthrange(today.year, (today.month + 1))[1]),
}


def my_job():
    sort_mailing()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def apscheduler(scheduler):
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        my_job,
        trigger=CronTrigger(second="*/5"),
        id="my_job",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'my_job'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
        "Added weekly job: 'delete_old_job_executions'."
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")


def send_distribution(mailing):
    status = True
    error_message = ''
    try:
        send_mail(
            subject=mailing.message.title,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False
        )
        error_message = 'OK'
    except SMTPException as error:
        status = False
        if 'authentication failed' in str(error):
            error_message = 'Ошибка аутентификации в почтовом сервисе'
        elif 'suspicion of SPAM' in str(error):
            error_message = 'Слишком много рассылок, сервис отклонил письмо'
        else:
            error_message = error
    finally:
        log = MailingLog.objects.create(
            status=status,
            server_response=error_message,
            mailing=mailing,
            owner=mailing.owner
        )
        log.save()


def sort_mailing():
    mailings: QuerySet = MailingSettings.objects.filter(is_active=True)
    current_time = timezone.now()
    now = current_time.strftime('%H:%M')
    for mailing in mailings:
        if mailing.end_time <= current_time:
            mailing.status = "Завершена"
            mailing.save()
        elif mailing.start_time > current_time:
            mailing.status = "Создана"
            mailing.save()
        elif mailing.start_time <= current_time < mailing.end_time:
            mailing.status = "Запущена"
            mailing.save()
            if MailingLog.objects.filter(mailing=mailing.pk).exists():
                delta = current_time - MailingLog.objects.filter(mailing=mailing.pk).last().time
                if mailing.start_time.strftime('%H:%M') == now and delta > PERIODICITY[mailing.periodicity]:
                    send_distribution(mailing)
            else:
                send_distribution(mailing)


def cache_extra_context():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    apscheduler(scheduler)
    if not CACHE_ENABLED:
        extra_context = {'object_list': Blog.objects.all().order_by('?')[:3],
                         'distributions_active': MailingSettings.objects.filter(is_active=True).count(),
                         'distributions': MailingSettings.objects.all().count(),
                         'clients_unique': Client.objects.values('email').distinct().count()}
        return extra_context
    key = "extra_context"
    extra_context = cache.get(key)
    if extra_context is None:
        extra_context = {'object_list': Blog.objects.all().order_by('?')[:3],
                         'distributions_active': MailingSettings.objects.filter(is_active=True).count(),
                         'distributions': MailingSettings.objects.all().count(),
                         'clients_unique': Client.objects.values('email').distinct().count()}
        cache.set(key, extra_context)
    return extra_context
