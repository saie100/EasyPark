from rest_framework import serializers
from .models import ParkingSpot, Reservations, AdminSetting

class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ['id', 'client_id', 'street_address', 'city', 'state', 'zip_code', 'vehicle_type', 'start_date', 'end_date', 'image', 'date_created', 'date_updated' ]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'client_id', 'renter_id', 'start_date', 'end_date', 'parking_spot_id', 'date_created', 'date_updated' ]

class AdminSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSetting
        fields = ['id', 'hourly_rate']

