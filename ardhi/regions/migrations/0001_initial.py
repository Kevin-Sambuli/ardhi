# Generated by Django 3.2.3 on 2021-06-14 09:57

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coucode', models.CharField(max_length=2, unique=True)),
                ('first_coun', models.CharField(max_length=30, unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'counties',
                'db_table': 'counties',
            },
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loccodeful', models.CharField(max_length=8)),
                ('first_locn', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'locations',
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='SubCounties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sccodefull', models.CharField(max_length=4)),
                ('first_scou', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'subcounties',
                'db_table': 'subcounties',
            },
        ),
        migrations.CreateModel(
            name='SubLocations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slcodefull', models.CharField(max_length=10)),
                ('first_slna', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'sublocations',
                'db_table': 'sublocations',
            },
        ),
    ]
