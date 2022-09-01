from django.db import models
from users.models import User


class ParkingSpot(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', blank=True, null=False)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True) #Truck, SUV, Car
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='parking_spot_images')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_updated']