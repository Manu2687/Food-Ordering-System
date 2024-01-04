# Generated by Django 5.0 on 2023-12-31 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=55)),
                ('img_name', models.CharField(max_length=55)),
                ('feature', models.CharField(max_length=90)),
                ('active', models.CharField(max_length=10)),
            ],
        ),
    ]