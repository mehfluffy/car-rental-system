# Generated by Django 3.2.4 on 2021-06-25 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiacar', '0010_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='amount',
            field=models.FloatField(choices=[(50.0, 'fifty_euro'), (20.0, 'twenty_euro'), (10.0, 'ten_euro'), (5.0, 'five_euro'), (2.0, 'two_euro'), (1.0, 'one_euro'), (0.5, 'fifty_cent'), (0.2, 'twenty_cent')]),
        ),
    ]
