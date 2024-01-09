# Generated by Django 5.0 on 2024-01-09 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_App', '0014_auto_20240109_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation_table',
            name='booking_name',
            field=models.CharField(default='default_name', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation_table',
            name='message',
            field=models.CharField(default='default-message', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation_table',
            name='total_person',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
