# Generated by Django 3.1.5 on 2021-02-05 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210204_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
