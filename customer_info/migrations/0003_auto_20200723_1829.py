# Generated by Django 3.0.5 on 2020-07-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_info', '0002_bank_detail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_detail',
            name='cust_FD',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bank_detail',
            name='cust_lone',
            field=models.IntegerField(default=0),
        ),
    ]