# Generated by Django 3.2.4 on 2021-06-24 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiacar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
