# Generated by Django 3.1.5 on 2021-02-16 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_auto_20210215_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
