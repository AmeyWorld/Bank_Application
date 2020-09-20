from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active='Y')

class InactiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active='N')

class Bank_Detail(models.Model):
    cust_acc_no = models.IntegerField(primary_key=True)
    cust_acc_type = models.CharField(max_length=200)
    cust_name = models.CharField(max_length=200)
    cust_age = models.IntegerField(null=True)
    cust_add = models.CharField(max_length=200, default="")
    dummy_add = models.CharField(max_length=200, default="")
    add_status = models.CharField(max_length=200, default="")

    req_money = models.IntegerField(default=0)
    req_money_name = models.CharField(max_length=200,default="")
    req_money_accNo = models.IntegerField(default=0)

    cust_balance = models.IntegerField()
    cust_lone = models.IntegerField(default=0)
    cust_FD = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active = models.CharField(default='Y', max_length=100)
    activeall = ActiveManager()
    inactiveall = InactiveManager()

    def __str__(self):
        return self.cust_name
