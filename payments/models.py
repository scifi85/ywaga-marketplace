from django.db import models
from paypal.standard.ipn.models import PayPalIPN
from django.contrib.auth.models import User

class Payment(models.Model):
    STATUS_CHOICES=(
        ('created', 'created'),
        ('wait', 'wait'),
        ('success', 'success'),
        ('failure', 'failure'),
        )
    PAYWAY_CHOICES=(
        ('liqpay', 'liqpay'),
        ('paypal', 'paypal'),
        )
    status = models.CharField(max_length=50,null=True, blank=True,choices=STATUS_CHOICES)
    pay_way = models.CharField(max_length=50,null=True, blank=True,choices=PAYWAY_CHOICES)
    sender_phone = models.CharField(max_length=50,null=True, blank=True)
    code = models.CharField(max_length=50,null=True, blank=True)
    amount = models.FloatField(max_length=50)
    currency = models.CharField(max_length=50,null=True, blank=True)
    description = models.CharField(max_length=500,null=True, blank=True)
    pay_details = models.CharField(max_length=50,null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    user = models.ForeignKey(User,null=True, blank=True)
    paypal = models.CharField("Transaction ID", max_length=19, blank=True, help_text="PayPal transaction ID.")
    invoice_id = models.CharField("Invoice ID", max_length=200, blank=True, help_text="Liqpay transaction ID.")