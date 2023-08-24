from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth.models import User

STATUS = [
    ("N", 'новый'),
    ("A", 'принят'),
]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ads(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    time_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_ads')

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.pk)])


class Reply(models.Model):
    reply = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS, default='N')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='ad_replies')
    time_creation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('reply_update', args=[str(self.pk)])


class Emails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    activate_code = models.IntegerField()


# class Subscription(models.Model):
#     user = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )
#     category = models.ForeignKey(
#         to='Category',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )
