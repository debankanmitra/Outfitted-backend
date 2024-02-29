"""
This file is used to handle requests and return responses. Each view function takes a request object and returns a response object.
"""

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import models
from .serializers import CartSerializer, ProductSerializer, UserDetailsSerializer,UserRegistrationSerializer,LoginSerializer

# Create your views here.

# ------------------------------ REGISTRATION ----------------------------------------------------
class UserRegistrationView(APIView):
    def post(self, request):
        # Receive the data from the client side
        datareceived=request.data
        email = datareceived.get('email')
        username = datareceived.get('username')
        password = datareceived.get('password')
        confirm_password = datareceived.get('confirm_password')
        # Check if data already exist or not
        if models.User.objects.filter(email=email).exists():
            error_response = {
                "message": "User with this email already exists."
            }
            return Response(error_response,status=status.HTTP_409_CONFLICT)
        elif models.User.objects.filter(username=username).exists():
            error_response = {
                "message": "User with this username already exists."
            }
            return Response(error_response,status=status.HTTP_409_CONFLICT)
        elif password != confirm_password:
            error_response = {
                "message": "Password fields didn't match."
            }
            return Response(error_response,status=status.HTTP_400_BAD_REQUEST)
        
        # Save the data in the database
        serializer = UserRegistrationSerializer(data=datareceived)
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

#TODO: CHECK if login needs the generated token on the header or not as it is a token based authetication it must need it else we have to implement
# For subsequent requests that require authentication, the client includes the token in the Authorization header of the HTTP request.
# we can also implement session based authentication instead of token based authentication 

class LoginView(APIView):
    permission_classes = [~IsAuthenticated]  # Allow only unauthenticated users

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)})
# -----------------------------------------------------------------------------------

class UserDetails(viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserDetailsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] # The AllowAny permission class allows unrestricted access, regardless of if the request was authenticated or unauthenticated.

    # The error message indicates that you're trying to use the @action decorator on a method (retrieve) that already exists in the GenericViewSet. 
    # The @action decorator is used to add extra actions to a GenericViewSet, but it cannot be used on methods that already exist in the GenericViewSet.
    @action(detail=False,methods=['GET']) #experimental
    def RetrieveAllUsers(self, _):
        queryset = models.User.objects.all()
        serializer= UserDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # @action(detail=False, methods=['post'])
    # def Createuser(self, request):

    #     # Receive the data from the client side
    #     datareceived=request.data
    #     serializer = UserDetailsSerializer(data=datareceived)

    #     # Check if data already exist or not
    #     if models.User.objects.filter(**datareceived).exists():
    #         error_response = {
    #         "error": {
    #             "code": 409,
    #             "message": "User already exists",
    #             "details": "The requested operation could not be completed because the user already exists."
    #         }
    #         }
    #         return Response(error_response,status=status.HTTP_409_CONFLICT)

    #     # Validate the data entered by the user
    #     if serializer.is_valid():
    #         serializer.save() # the save() method is called on the serializer. This method saves the deserialized data to the database. It creates a new UserDetails object with the validated data and saves it to the database.
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    #  The detail=True argument means that this action operates on a single instance of the model, identified by the primary key (pk)
    #  The detail=False argument means to indicate that this is not a detail route, and the URL does not need a specific user identifier.
    @action(detail=False,methods=['patch'])
    def PatchUserDetail(self,request):
        user = request.user  # The authenticated user
        serializer = UserDetailsSerializer(instance=user,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
            "message": "user details saved successfully"
            }
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------------------------
# ask: https://www.phind.com/agent?cache=clt4estfv000pky08ok0p9moz
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        query = models.Product.objects.all()
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)
        


# -------------------------------------------------------------------------------------------------------------------
class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        query, _ = models.Cart.objects.filter(user=user)
        serializer = CartSerializer(query)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        query, _ = models.Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = CartSerializer(instance=user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        user = request.user
        try:
            cart_item = models.Cart.objects.get(id=item_id, cart__user=user)
            cart_item.delete()
            return Response({"detail": "Cart item deleted successfully."}, status=200)
        except cart_item.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=404)

