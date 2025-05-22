from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count, Case, When, IntegerField, Sum
from . import serializers
from . import models
from .filters import StaffFilter


import logging

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.MyTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserMeAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    
class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class=serializers.UserSerializer
    queryset=models.CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field='id'

class DeleteUserAPIView(generics.DestroyAPIView):
    serializer_class=serializers.UserSerializer
    queryset=models.CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field='id'

class CreateUserAPIView(generics.CreateAPIView):
    serializer_class=serializers.UserSerializer
    queryset=models.CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    

class ListUserAPIView(generics.ListAPIView):
    serializer_class=serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends=[DjangoFilterBackend, SearchFilter,]
    filterset_class = StaffFilter
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

