from http import client
from tracemalloc import start
from django.shortcuts import render
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from users.models import User
from payment_interface.models import PaymentInterface
from users.serializers import UserSerializer
from payment_interface.serializers import PaymentInterfaceSerializer

class PaymentInterfaceView(viewsets.ModelViewSet):
    queryset = PaymentInterface.objects.all()
    serializer_class = PaymentInterfaceSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        bank_name = request.data['bank_name']
        routing_number = request.data['routing_number']
        account_number = request.data['account_number']

        new_spot = PaymentInterface.objects.create(user=request.user, bank_name=bank_name,routing_number=routing_number,account_number=account_number)
        new_spot.save()
        Response("New Payment Created")

    def list(self, request):
        
        self.queryset = PaymentInterface.objects.get(user=request.user)
        return Response(self.serializer_class(self.queryset, many=False).data)

