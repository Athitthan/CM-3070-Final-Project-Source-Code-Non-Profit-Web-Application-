# Generated by Django 3.2.19 on 2023-08-25 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysocialapp', '0003_appuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='username',
        ),
    ]
