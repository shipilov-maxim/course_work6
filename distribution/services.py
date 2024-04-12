from smtplib import SMTPException
import logging
from django.conf import settings
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta
from django.db.models import QuerySet
from django_apscheduler.jobstores import DjangoJobStore
from config import settings
from distribution.models import MailingSettings, MailingLog
from django.utils import timezone

logger = logging.getLogger(__name__)


def my_job():
    sort_mailing()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def apscheduler(scheduler):
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        my_job,
        trigger=CronTrigger(second="*/10"),
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
        status = True
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
        )
        log.save()


def sort_mailing():
    active_mailings: QuerySet = MailingSettings.objects.exclude(status='Завершена')
    current_time = timezone.localtime(timezone.now())
    now_utc = (timezone.now()).strftime('%H:%M')
    for mailing in active_mailings:
        if mailing.end_time <= current_time:
            mailing.status = "Завершена"
            mailing.save()
        elif mailing.start_time <= current_time < mailing.end_time:
            mailing.status = "Запущена"
            mailing.save()

            #                 today = datetime.today()
            #                 days = calendar.monthrange(today.year, today.month)[1]
            #                 mailing.next_send = current_time + timedelta(days=days)

            if mailing.start_time.strftime('%H:%M') == now_utc:
                send_distribution(mailing)
