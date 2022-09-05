from django.db import models

class PaymentInterface(models.Model):
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    routing_number = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
