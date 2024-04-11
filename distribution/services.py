from smtplib import SMTPException
import logging
import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta
from django.db.models import QuerySet
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from distribution.models import MailingSettings, MailingLog
from django.utils import timezone


def my_job():
    # print('hello')
    sort_mailing()


logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def apscheduler(scheduler):
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        my_job,
        trigger=CronTrigger(second="*/10"),  # Every 10 seconds
        id="my_job",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'my_job'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
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


def sort_mailing():
    active_mailings: QuerySet = MailingSettings.objects.exclude(status='Завершена')
    current_time = timezone.localtime(timezone.now())
    now = current_time.strftime('%Y-%m-%d %H:%M')
    for mailing in active_mailings:
        if mailing.end_time <= current_time:
            mailing.status = "Завершена"
            mailing.save()
        elif mailing.start_time.strftime('%Y-%m-%d %H:%M') <= now < mailing.end_time.strftime('%Y-%m-%d %H:%M'):
            mailing.status = "Запущена"
            mailing.save()

    #                 today = datetime.today()
    #                 days = calendar.monthrange(today.year, today.month)[1]
    #                 mailing.next_send = current_time + timedelta(days=days)
    #
    #             status = True
    #             error_message = ''
    #             try:
    #                 send_mail(
    #                     subject=mailing.message.title,
    #                     message=mailing.message.text,
    #                     from_email=settings.EMAIL_HOST_USER,
    #                     recipient_list=[client.email for client in mailing.clients.all()],
    #                     fail_silently=False
    #                 )
    #                 status = True
    #                 error_message = 'OK'
    #             except SMTPException as error:
    #                 status = False
    #                 if 'authentication failed' in str(error):
    #                     error_message = 'Ошибка аутентификации в почтовом сервисе'
    #                 elif 'suspicion of SPAM' in str(error):
    #                     error_message = 'Слишком много рассылок, сервис отклонил письмо'
    #                 else:
    #                     error_message = error
    #             finally:
    #                 log = MailingLog.objects.create(
    #                     status=status,
    #                     server_response=error_message,
    #                     mailing=mailing,
    #                     owner=mailing.owner
    #                 )
    #                 log.save()
