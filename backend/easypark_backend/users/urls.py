from django.urls import path
from .views import DeleteAccount, SignIn, SignOut, SignUp, UpdateAccount, UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'signup', SignUp)
router.register(r'signin', SignIn)
router.register(r'signout', SignOut)
router.register(r'update', UpdateAccount)
router.register(r'delete', DeleteAccount)

router.register(r'', UserView)
urlpatterns = router.urls