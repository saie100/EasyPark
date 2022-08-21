from django.urls import path
from .views import SignIn, SignOut, SignUp, UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'signup', SignUp)
router.register(r'signin', SignIn)
router.register(r'signout', SignOut)
router.register(r'', UserView)
urlpatterns = router.urls