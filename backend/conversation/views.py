from rest_framework import status, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer()
    post = serializer.create(request.user.family_id)
    data = {"id": post.id}
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_post(request):
    serializer = PostSerializer()
    post = Post.objects.get(id=request.data["id"])
    data = {
        "content": "content",
        "emotion": 1,
        "keyword": "keyword"
    }
    serializer.update(post=post, data=data)
    return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]