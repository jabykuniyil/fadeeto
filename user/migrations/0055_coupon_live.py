# Generated by Django 3.1.5 on 2021-03-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0054_auto_20210301_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='live',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
