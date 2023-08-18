import random
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Emails


@receiver(post_save, sender=User)
def to_verify_emails(instance, created, **kwargs):
    if created:
        Emails.objects.create(user=instance, is_verified=False, activate_code=random.randrange(10000, 100000))
        # send_code(instance)


def send_code(user_id):
    instance = Emails.objects.get(user_id=user_id)
    code = instance.activate_code
    user = User.objects.get(id=user_id)

    to_email = user.email
    subject = 'Код доступа'
    html_content = render_to_string('mails/mail_code.html', {'code': code})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, None, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
