from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

""" 
[signup api]
    username: char
    password: char
    email: char
    first_name: char
    last_name: char
    phone_number: char
    birth: YY-MM-DD
    is_senior: 0(unknown)/1(male)/2(female)
[login api]
    username: char
    password: char
"""

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        token = Token.objects.get(user=user)
        data = {
            "user": serializer.data,
            "token": token.key
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    authenticate_user = authenticate(username=request.data['username'], password=request.data['password'])

    if authenticate_user is not None:
        user = User.objects.get(username=request.data['username'])
        serializer = UserSerializer(user)
        response_data = {
            'user': serializer.data,
        }
        token, created_token = Token.objects.get_or_create(user=user)
        if token:
            response_data['token'] = token.key
        elif created_token:
            response_data['token'] = created_token.key

        return Response(response_data, status=status.HTTP_202_ACCEPTED)
    return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "logout was successful"})