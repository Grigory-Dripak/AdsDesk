from celery.app import shared_task
from .management.commands.runapscheduler import my_job
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_notifications(subject, text_content, html_content, mails_list):
    for email in set(mails_list):
         msg = EmailMultiAlternatives(subject, text_content, None, [email])
         msg.attach_alternative(html_content, "text/html")
         msg.send()


@shared_task
def send_weekly_ads():
    my_job()
