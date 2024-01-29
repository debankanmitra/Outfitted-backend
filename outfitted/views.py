"""
This file is used to handle requests and return responses. Each view function takes a request object and returns a response object.
"""

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models
from . import serializers

# Create your views here.



class UserDetails(viewsets.GenericViewSet):
    queryset = models.UserDetails.objects.all()
    serializer_class = serializers.UserDetailsSerializer
    permission_classes = [AllowAny] # The AllowAny permission class allows unrestricted access, regardless of if the request was authenticated or unauthenticated.

    # The error message indicates that you're trying to use the @action decorator on a method (retrieve) that already exists in the GenericViewSet. 
    # The @action decorator is used to add extra actions to a GenericViewSet, but it cannot be used on methods that already exist in the GenericViewSet.
    def retrieve(self, request):
        queryset = models.UserDetails.objects.all()
        serializer=serializers.UserDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def Createuser(self, request):
        serializer = serializers.UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # the save() method is called on the serializer. This method saves the deserialized data to the database. It creates a new UserDetails object with the validated data and saves it to the database.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


    

    