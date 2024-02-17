from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from sheduler.models import Mail, Logs


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    weak = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mailings = Mail.objects.all().filter(status='created') \
        .filter(is_active=True) \
        .filter(next_date__lte=datetime.now(pytz.timezone('Europe/Moscow'))) \
        .filter(end_date__gte=datetime.now(pytz.timezone('Europe/Moscow')))

    for mail in mailings:
        mail.status = 'start'
        mail.save()
        emails_list = [client.email for client in mail.client.all()]

        result = send_mail(
            subject=mail.message.title,
            message=mail.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )

        if result == 1:
            status = 'finish'
        else:
            status = 'error'

        log = Logs(mailing=Mail, status=status)
        log.save()

        if mail.interval == 'once_a_day':
            mail.next_date = log.last_mailing_time + day
        elif mail.interval == 'once_a_week':
            mail.next_date = log.last_mailing_time + weak
        elif mail.interval == 'once_a_month':
            mail.next_date = log.last_mailing_time + month

        if mail.next_date < mail.end_date:
            mail.status = 'created'
        else:
            mail.status = 'finish'
        mail.save()


def get_cache_for_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mail.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mail.objects.all().count()
    return mailings_count


def get_cache_for_active_mailings():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mail.objects.filter(is_active=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mail.objects.filter(is_active=True).count()
    return active_mailings_count