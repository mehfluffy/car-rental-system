# Generated by Django 3.2.4 on 2021-06-24 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subtype',
            fields=[
                ('subtype_name', models.CharField(choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('L4', 'L4'), ('L5', 'L5'), ('L6', 'L6'), ('L7', 'L7'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('O1', 'O1'), ('O2', 'O2'), ('O3', 'O3'), ('O4', 'O4'), ('T', 'T'), ('G', 'G'), ('SA', 'SA'), ('SB', 'SB'), ('SC', 'SC'), ('SD', 'SD')], max_length=2, primary_key=True, serialize=False)),
                ('hourprice_gold', models.FloatField()),
                ('hourprice_reg', models.FloatField()),
                ('pledgeprice_reg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.CharField(choices=[('G', 'Gold'), ('R', 'Regular')], default='R', max_length=1)),
                ('username', models.CharField(max_length=11, null=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('delays_thismonth', models.IntegerField(default=0)),
                ('is_renting', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('park_location', models.CharField(max_length=5)),
                ('available', models.BooleanField(default=True)),
                ('subtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asiacar.subtype')),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('price_predelay', models.FloatField()),
                ('time_returned', models.DateTimeField(default=None)),
                ('price_total', models.FloatField()),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asiacar.user')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asiacar.vehicle')),
            ],
        ),
    ]
