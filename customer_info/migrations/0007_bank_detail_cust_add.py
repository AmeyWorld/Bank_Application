# Generated by Django 3.0.5 on 2020-07-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_info', '0006_auto_20200725_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_detail',
            name='cust_add',
            field=models.CharField(default='', max_length=200),
        ),
    ]