# Generated by Django 3.1.5 on 2021-02-10 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_delete_vendorturf'),
        ('user', '0021_turf_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor'),
        ),
    ]
