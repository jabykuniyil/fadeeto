# Generated by Django 3.1.5 on 2021-03-02 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0057_auto_20210302_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]