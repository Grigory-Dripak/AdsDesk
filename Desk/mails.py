from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tasks import send_notifications
from .models import Emails, Ads


def send_code(user_id):
    instance = Emails.objects.get(user_id=user_id)
    code = instance.activate_code
    user = User.objects.get(id=user_id)

    to_email = user.email
    subject = 'Код доступа'
    html_content = render_to_string('mails/mail_code.html', {'code': code})
    text_content = strip_tags(html_content)

    send_notifications.delay(
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        mails_list=to_email
    )


def reply_notification(user_id, author, text):
    receiver = User.objects.get(id=user_id)
    author = User.objects.get(id=author).username
    message = f'От {author} получен новый отклик к вашей публикации. \n Текст отклика: "{text}"'

    to_email = receiver.email
    subject = f'Отклик на ваше объявление'
    html_content = render_to_string('mails/newreply.html', {'message': message})
    text_content = strip_tags(html_content)

    send_notifications.delay(
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        mails_list=to_email
    )


def status_notification(user_id, ad_pk, status):
    user = User.objects.get(id=user_id)
    ad = Ads.objects.get(id=ad_pk)
    text = f'Ваш отклик к публикации "{ad.title}" из раздела "{ad.category}" был'

    if status == 'D':
        message = f'{text} отклонен'
    elif status == 'A':
        message = f'{text} принят'
    else:
        message = 'Сменился статус отклика.'

    to_email = user.email
    subject = 'Статус отклика'
    html_content = render_to_string('mails/reply_status.html', {'message': message})
    text_content = strip_tags(html_content)

    send_notifications.delay(
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        mails_list=to_email
    )
