# Generated by Django 3.1.5 on 2021-02-25 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0043_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='latitude',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='turf',
            name='longitude',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
