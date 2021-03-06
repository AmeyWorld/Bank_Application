# Generated by Django 3.0.5 on 2020-07-23 12:38

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Detail',
            fields=[
                ('cust_acc_no', models.IntegerField(primary_key=True, serialize=False)),
                ('cust_acc_type', models.CharField(max_length=200)),
                ('cust_name', models.CharField(max_length=200)),
                ('cust_age', models.IntegerField()),
                ('cust_balance', models.IntegerField()),
                ('cust_lone', models.IntegerField()),
                ('cust_FD', models.IntegerField()),
                ('active', models.CharField(default='Y', max_length=100)),
            ],
            managers=[
                ('activeall', django.db.models.manager.Manager()),
            ],
        ),
    ]
