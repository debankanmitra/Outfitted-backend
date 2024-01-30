"""
This file is used to handle requests and return responses. Each view function takes a request object and returns a response object.
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models
from .serializers import UserDetailsSerializer

# Create your views here.



class UserDetails(viewsets.GenericViewSet):
    queryset = models.UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [AllowAny] # The AllowAny permission class allows unrestricted access, regardless of if the request was authenticated or unauthenticated.

    # The error message indicates that you're trying to use the @action decorator on a method (retrieve) that already exists in the GenericViewSet. 
    # The @action decorator is used to add extra actions to a GenericViewSet, but it cannot be used on methods that already exist in the GenericViewSet.
    @action(detail=False,methods=['GET'])
    def RetrieveAllUsers(self, request):
        queryset = models.UserDetails.objects.all()
        serializer= UserDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def Createuser(self, request):

        # Receive the data from the client side
        datareceived=request.data
        serializer = UserDetailsSerializer(data=datareceived)

        # Check if data already exist or not
        if models.UserDetails.objects.filter(**datareceived).exists():
            error_response = {
            "error": {
                "code": 409,
                "message": "User already exists",
                "details": "The requested operation could not be completed because the user already exists."
            }
            }
            return Response(error_response,status=status.HTTP_409_CONFLICT)

        # Validate the data entered by the user
        if serializer.is_valid():
            serializer.save() # the save() method is called on the serializer. This method saves the deserialized data to the database. It creates a new UserDetails object with the validated data and saves it to the database.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    #  The detail=True argument means that this action operates on a single instance of the model, identified by the primary key (pk)
    @action(detail=True,methods=['patch'])
    def PatchUserDetail(self,request,pk):
        user= models.UserDetails.objects.get(pk=pk)
        serializer = UserDetailsSerializer(instance=user,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
            "message": f"New item added to Cart with id: {user.id}"
            }
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

