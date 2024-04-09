from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(request.user.family_id)
        data = {"event": serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_event(request, date):
    print(date)
    queryset = Event.objects.filter(
        Q(family_id=request.user.family_id) &
        Q(datetime__date=date)
    )
    serializer = EventSerializer(queryset, many=True)
    data = {"events": serializer.data}
    return Response(data)
