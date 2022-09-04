from django.urls import path
from .views import PaymentInterfaceView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PaymentInterfaceView)
urlpatterns = router.urls