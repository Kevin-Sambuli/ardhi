# Generated by Django 3.2.3 on 2021-06-28 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertySearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parcel', models.CharField(max_length=10, verbose_name='Parcel')),
                ('purpose', models.TextField(max_length=200, verbose_name='Purpose')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Land Search',
                'verbose_name_plural': 'Land Search',
                'db_table': 'landsearch',
            },
        ),
    ]
