from smtplib import SMTPException
from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta
from django.db.models import QuerySet
from config import settings
from distribution.models import MailingSettings, MailingLog
from django.utils import timezone


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
