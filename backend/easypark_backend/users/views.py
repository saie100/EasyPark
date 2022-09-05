from hashlib import new
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        """queryedUser = request.GET.get('email', '')

        if(User.objects.filter(email=queryedUser).exists()):
            self.queryset = User.objects.get(email=queryedUser)
            return Response(self.serializer_class(self.queryset, many=False).data)

        elif(queryedUser != ''):
            return Response("User does not exist")

        else:        
            self.queryset = User.objects.all()
            return Response(self.serializer_class(self.queryset, many=True).data)
"""      
        self.queryset = User.objects.all()
        print(request.user)
        print(request)
        return Response(self.serializer_class(self.queryset, many=True).data)

class SignUp(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        username = request.data['email']

        new_user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
        new_user.set_password(request.data['password'])
        new_user.save()

        return Response("New User Created")

class SignIn(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        
        user = authenticate(request=request, username=request.data['email'], password=request.data['password'])

        if(user is not None):
            login(request, user)
            request.session.modified = True
            resp = Response("User Logged In")
            return resp
        else:
            return Response("Wrong Credentials")

class SignOut(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def list(self, request):
        logout(request)
        print("Logged Off")
        resp = Response("Logged out")
        return resp











