# Generated by Django 3.0.5 on 2020-07-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_info', '0004_auto_20200725_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_detail',
            name='cust_age',
            field=models.IntegerField(),
        ),
    ]
