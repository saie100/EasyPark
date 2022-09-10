from http import client
import re
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
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ParkingSpotView(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        client = request.user
        street_address = request.data['street_address']
        city = request.data['city']
        state = request.data['state']
        zip_code = request.data['zip_code']
        vehicle_type = request.data['vehicle_type']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        start_time = request.data['start_time']
        end_time = request.data['end_time']
        image = request.data['image']
        
        print(image)
        new_start_date = datetime.strptime(start_date + " " + start_time+":00", "%Y-%m-%d %H:%M:%S")
        new_end_date = datetime.strptime(end_date + " " + end_time+":00", "%Y-%m-%d %H:%M:%S")

        try:
            new_spot = ParkingSpot.objects.create(client=client, image=image, street_address=street_address, city=city, state=state, zip_code=zip_code, vehicle_type=vehicle_type, start_date=new_start_date, end_date=new_end_date)
            new_spot.save()
            return Response("New Spot Created")
        except:
            return Response("Something went wrong in the backend")
    
    def list(self, request):
        self.queryset = ParkingSpot.objects.filter().order_by('-id')[:2]
        #self.queryset = ParkingSpot.objects.all()
        return Response(self.serializer_class(self.queryset, many=True).data)
