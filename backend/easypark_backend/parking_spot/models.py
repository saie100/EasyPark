from distutils.command.upload import upload
from django.db import models
from users.models import User


class ParkingSpot(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True) #Compact, SUV, Standard, and Oversized
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/garage/')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        ordering = ['-date_updated']


class Reservations(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', blank=True, null=False)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter', blank=True, null=False)
    time_slot_usage = models.IntegerField() # In increments of hours
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, blank=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-date_updated']