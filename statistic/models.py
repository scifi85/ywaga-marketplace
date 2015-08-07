from django.db import models

# Create your models here.
class BalanceManager(models.Manager):
    def addToBalance(self,amount):
        amount=float(amount)
        all=Balance.objects.all()
        if all:
            balance=all[0]
        else:
            balance=Balance.objects.create(inAmount=0,outAmount=0,commission=0)

        balance.inAmount+=amount
        balance.save()

    def outFromBalance(self,amount):
        all=Balance.objects.all()
        if all:
            balance=all[0]
        else:
            balance=Balance.objects.create(inAmount=0,outAmount=0,commission=0)
        balance.outAmount+=amount
        balance.save()

    def commission(self,amount):
        all=Balance.objects.all()
        if all:
            balance=all[0]
        else:
            balance=Balance.objects.create(inAmount=0,outAmount=0,commission=0)
        balance.commission+=amount
        balance.save()

    def show(self):
        all=Balance.objects.all()
        if all:
            balance=all[0]
        else:
            balance=Balance.objects.create(inAmount=0,outAmount=0,commission=0)
        return balance

class Balance(models.Model):
    inAmount = models.FloatField(blank=True,null=True)
    outAmount = models.FloatField(blank=True,null=True)
    commission = models.FloatField(blank=True,null=True)
    objects = BalanceManager()

    def balance(self):
        return self.inAmount-self.outAmount

