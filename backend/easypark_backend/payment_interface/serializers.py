from rest_framework import serializers
from .models import PaymentInterface

class PaymentInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInterface
        fields = ['bank_name','routing_number','account_number','amount']