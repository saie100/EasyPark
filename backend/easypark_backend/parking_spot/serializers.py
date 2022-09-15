from rest_framework import serializers
from .models import ParkingSpot, Reservations, AdminSetting
from users.models import User
from users.serializers import UserSerializer


class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ['id', 'client_id', 'street_address', 'city', 'state', 'zip_code', 'start_date', 'end_date', 'image', 'date_created', 'date_updated' ]

class ReservationSerializer(serializers.ModelSerializer):
    renter = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    parking_spot = ParkingSpotSerializer(read_only=True)
    
    class Meta:
        model = Reservations
        fields = ['id', 'client', 'client_id', 'renter', 'renter_id', 'parking_spot', 'parking_spot_id', 'start_date', 'end_date', 'date_created', 'date_updated' ]

class AdminSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSetting
        fields = ['id', 'hourly_rate']

