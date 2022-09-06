from rest_framework import serializers
from .models import ParkingSpot

class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ['id', 'client_id', 'street_address', 'city', 'state', 'zip_code', 'vehicle_type', 'start_date', 'end_date', 'image', 'date_created', 'date_updated' ]

