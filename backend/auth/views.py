from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, FamilySerializer

""" 
[signup api]
    username: char
    password: char
    email: char
    first_name: char
    last_name: char
    phone_number: char
    birth: YY-MM-DD
    is_senior: true/false
[login api]
    username: char
    password: char
[create-family api]
    family_name: char
    senior_gender: 0(unknown)/1(male)/2(female)
    senior_diseases: char
    senior_interests: char
[join-family]
    family_id: uuid(6)
    role: char
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
    data = {"error": serializer.errors}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    authenticate_user = authenticate(username=request.data['username'], password=request.data['password'])
    if authenticate_user is not None:
        user = User.objects.get(username=request.data['username'])
        serializer = UserSerializer(user)
        data = {'user': serializer.data,}
        token, created_token = Token.objects.get_or_create(user=user)
        if token:
            data['token'] = token.key
        elif created_token:
            data['token'] = created_token.key
        return Response(data, status=status.HTTP_202_ACCEPTED)
    data = {"error": "user not found"}
    return Response(data, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.user:
        request.user.auth_token.delete()
        data = {"message": "logout was successful"}
        return Response(data, status=status.HTTP_200_OK)
    data = {"error": "user not login"}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_family(request):
    serializer = FamilySerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        serializer.create(user=user)
        data = {
            "family": serializer.data,
            "role": "senior"
        }
        return Response(data, status=status.HTTP_201_CREATED)
    data = {"error": serializer.errors}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_family(request):
    try:
        serializer = UserSerializer()
        serializer.join(request.user, request.data)
        data = {"message": "join was successful"}
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        data = {"error": e}
        return Response(data, status=status.HTTP_404_NOT_FOUND)