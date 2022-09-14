from http import client
import re
from tracemalloc import start
from django.shortcuts import render
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from users.models import User
from parking_spot.models import AdminSetting, ParkingSpot, Reservations
from users.serializers import UserSerializer
from parking_spot.serializers import AdminSettingSerializer, ParkingSpotSerializer, ReservationSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
from datetime import date
from PIL import Image
from django.core.files.base import ContentFile

API_KEY = 'bZjyuUI32kAR1Ewm2snYZsi6SLF0TYTu5BV9NnZeqSarSMXURzS2RCKogOvx05MJ'

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
        image = request.FILES['media']
        
        file_content = ContentFile(image.read())
        
        new_start_date = datetime.strptime(start_date + " " + start_time+":00", "%Y-%m-%d %H:%M:%S")
        new_end_date = datetime.strptime(end_date + " " + end_time+":00", "%Y-%m-%d %H:%M:%S")

        try:
            new_spot = ParkingSpot.objects.create(client=client, street_address=street_address, city=city, state=state, zip_code=zip_code, vehicle_type=vehicle_type, start_date=new_start_date, end_date=new_end_date)
            new_spot.image.save(str(new_spot.id)+'.jpg', file_content, save=False)
            new_spot.save()
            return Response("New Spot Created")
        except:
            return Response("Something went wrong in the backend")
    
    def list(self, request):

        if(request.GET.get('client') == 'yes'):
            self.queryset = ParkingSpot.objects.filter(client=request.user).order_by('-date_created')[:2]
            return Response(self.serializer_class(self.queryset, many=True).data)
        else:
            print(request.GET.get('date') )
            
            if(request.GET.get('date')):
                start_end_date = request.GET.get('date')
                
                start_date = start_end_date.split("/")[0]
                end_date = start_end_date.split("/")[1]

                start = datetime.strptime(start_date+":00", "%Y-%m-%d:%H:%M:%S")
                end = datetime.strptime(end_date+":00", "%Y-%m-%d:%H:%M:%S")

                zip_code_values = list(ParkingSpot.objects.filter(start_date__lte=start).filter(end_date__gte=end).values_list('zip_code', flat=True))
                print(zip_code_values)
                self.queryset = ParkingSpot.objects.filter(zip_code__in=zip_code_values).order_by('-id')[:2]
                
                #self.queryset = ParkingSpot.objects.filter().order_by('-id')[:2]
            
                return Response(self.serializer_class(self.queryset, many=True).data)
            else:
                return Response("Something went wrong")


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        renter = request.user
        client_id = int(request.data['client_id'])
        parking_spot_id = int(request.data['parking_spot_id'])
        start_time = request.data['start_time']
        end_time = request.data['end_time']
        
        
        new_start_time = datetime.strptime(str(date.today()) + " " + start_time+":00", "%Y-%m-%d %H:%M:%S")
        new_end_time = datetime.strptime(str(date.today()) + " " + end_time+":00", "%Y-%m-%d %H:%M:%S")


        client = User.objects.get(id=client_id)
        parking_spot = ParkingSpot.objects.get(id=parking_spot_id)
        
        try:
            new_reservation = Reservations.objects.create(renter=renter, client=client, parking_spot=parking_spot, start_date=new_start_time, end_date=new_end_time)
            new_reservation.save()
            return Response("Reservation Created")
        except:
            return Response("Something went wrong in the backend")


    def list(self, request):
        
        if(request.GET.get('renter') == 'yes'):
            self.queryset = ParkingSpot.objects.filter(renter=request.user).order_by('-date_created')[:2]
            return Response(self.serializer_class(self.queryset, many=True).data)
        else:
            self.queryset = ParkingSpot.objects.filter(client=request.user).order_by('-date_created')[:2]
            return Response(self.serializer_class(self.queryset, many=True).data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AdminView(viewsets.ModelViewSet):
    queryset = AdminSetting.objects.all()
    serializer_class = AdminSettingSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        user = request.user
        rate = request.data['hourly_rate']

        if(AdminSetting.objects.filter(id=1).exists()):
            setting = AdminSetting.objects.get(id=1)
            setting.hourly_rate = rate
            setting.save()
            return Response("Updated hourly rate")
        else:
            AdminSetting.objects.create(hourly_rate=rate).save()
            return Response("Created new hourly rate")


    def list(self, request):
        if(AdminSetting.objects.filter(id=1).exists()):
            self.queryset = AdminSetting.objects.get(id=1)
            return Response(self.serializer_class(self.queryset, many=False).data)

        else:
            return Response("Hourly rate does not exist")

        