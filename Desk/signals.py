import random

from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Emails


@receiver(post_save, sender=User)
def to_verify_emails(instance, created, **kwargs):
    if created:
        Emails.objects.create(user=instance, is_verified=False, activate_code=random.randrange(111111, 1000000))
