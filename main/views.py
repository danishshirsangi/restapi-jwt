import http
import json
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from django.contrib.auth.models import User

from .serializer import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from main import serializer



# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def home_view(request):
    return Response({"message":"Logged In"})

@api_view(['GET','POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def register_user(request):
    print(request.user.id)
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        users = request.data
        serializer = UserSerializer(data=users)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            refresh = RefreshToken.for_user(user)
            return Response({"data":serializer.data,"refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
    return Response({"message":"hello world!"})

@api_view(['GET','POST'])
def login_user(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        usersin = request.data
        serializer = LoginSerializer(data=usersin)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.data['username']).exists():
                user = User.objects.get(username=serializer.data['username'])
                if user.check_password(serializer.data['password']):
                    refresh = RefreshToken.for_user(user)
                    return Response({"refresh":str(refresh),"access":str(refresh.access_token)}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":"Password Does not match"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"Username Does not match"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)