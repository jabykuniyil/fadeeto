# Generated by Django 3.1.5 on 2021-02-26 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0046_auto_20210226_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='turf',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
    ]
