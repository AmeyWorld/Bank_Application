# Generated by Django 3.0.5 on 2020-07-30 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_info', '0010_bank_detail_req_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_detail',
            name='req_money_accNo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bank_detail',
            name='req_money_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
