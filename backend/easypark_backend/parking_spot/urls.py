from django.urls import path
from .views import ParkingSpotView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ParkingSpotView)
urlpatterns = router.urls