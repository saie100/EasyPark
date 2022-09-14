from django.urls import path
from .views import ParkingSpotView, ReservationView, AdminView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reserve', ReservationView)
router.register(r'admin', AdminView)
router.register(r'', ParkingSpotView)



urlpatterns = router.urls