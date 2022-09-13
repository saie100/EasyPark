from django.db import models
from users.models import User

class PaymentInterface(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank', blank=True, null=False)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    routing_number = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)