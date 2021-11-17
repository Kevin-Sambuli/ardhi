# Generated by Django 3.2.3 on 2021-11-16 12:48

import datetime
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcels',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('perimeter', models.FloatField(max_length=10, verbose_name='Perimeter')),
                ('area_ha', models.FloatField(max_length=10, verbose_name='Area')),
                ('lr_no', models.CharField(max_length=10, verbose_name='LR Number')),
                ('status', models.CharField(choices=[('on_sale', 'on sale'), ('in_use', 'in use')], default='in_use', max_length=10, verbose_name='Status')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name_plural': 'parcels',
                'db_table': 'parcels',
            },
        ),
        migrations.CreateModel(
            name='ParcelDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_use', models.CharField(choices=[('A', 'Agricultural'), ('R', 'Residential'), ('C', 'Commercial'), ('RC', 'Recreational'), ('T', 'Transport')], default=None, max_length=15, verbose_name='Land_use')),
                ('tenure', models.CharField(choices=[('freehold', 'Freehold'), ('leasehold', 'Leasehold')], default=None, max_length=10, verbose_name='Tenure')),
                ('improvements', models.CharField(default='nil', max_length=100, verbose_name='Land Improvements')),
                ('encumbrances', models.CharField(default='nil', max_length=100, verbose_name='Encumbrances')),
                ('purchase_date', models.DateTimeField(verbose_name='Purchase Date')),
                ('registered', models.DateTimeField(default=datetime.datetime.now)),
                ('parcel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', related_query_name='details', to='parcels.parcels', verbose_name='Parcels')),
            ],
            options={
                'verbose_name_plural': 'parcel_details',
                'db_table': 'parcel_details',
            },
        ),
    ]
