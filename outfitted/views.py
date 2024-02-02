"""
This file is used to handle requests and return responses. Each view function takes a request object and returns a response object.
"""

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import models
from .serializers import UserDetailsSerializer,UserRegistrationSerializer,LoginSerializer

# Create your views here.

# ------------------------------ REGISTRATION ----------------------------------------------------
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(attrs=serializer.validated_data)
            return Response({'message': 'User created successfully.'}, status=201)
        return Response(serializer.errors, status=400)
# ----------------------------------- LOGIN -------------------------------------
# Upon receiving a request with an "Authorization" header, your API server performs token verification:
# It extracts the token value from the header.
# It validates the token's authenticity and integrity (e.g., using signature verification in complex token systems).
# If valid, it retrieves the user associated with that token from the database.
# If the token is valid and corresponds to an active user, the server grants access to the requested resource or endpoint based on the user's permissions.
# The user can continue interacting with the API without needing to re-enter their credentials for each request.

class LoginView(APIView):
    permission_classes = [~IsAuthenticated]  # Allow only unauthenticated users

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
# -----------------------------------------------------------------------------------

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
            "message": f"user details edited with id: {user.id}"
            }
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

