# Generated by Django 3.2.4 on 2021-07-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiacar', '0011_alter_money_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='license_number',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
