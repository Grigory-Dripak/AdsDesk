# Generated by Django 4.2.4 on 2023-08-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Desk', '0003_remove_ads_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='status',
            field=models.CharField(choices=[('N', 'новый'), ('A', 'принят')], default='N', max_length=1),
        ),
    ]
