from http import client
from tracemalloc import start
from django.shortcuts import render
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from users.models import User
from parking_spot.models import ParkingSpot
from users.serializers import UserSerializer
from parking_spot.serializers import ParkingSpotSerializer

class ParkingSpotView(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        client = request.user
        street_address = request.data['street_address']
        city = request.data['city']
        state = request.data['state']
        zip_code = request.data['zip_code']
        vehicle_type = request.data['vehicle_type']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        available = request.data['available']

        new_spot = ParkingSpot.objects.create(client=client, street_address=street_address, city=city, state=state, zip_code=zip_code, vehicle_type=vehicle_type, start_date=start_date, end_date=end_date, available=available)
        new_spot.save()
        Response("New Spot Created")

    def list(self, request):
        
        self.queryset = ParkingSpot.objects.all()
        return Response(self.serializer_class(self.queryset, many=True).data)
