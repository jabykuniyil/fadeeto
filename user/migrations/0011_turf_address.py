# Generated by Django 3.1.5 on 2021-02-05 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_turf_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='address',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]