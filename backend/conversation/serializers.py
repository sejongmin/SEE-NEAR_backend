from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from .models import Post
from authentication.models import Family

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ("id",)

    def create(self, family):
        family = Family.objects.get(id=family)
        new_post = Post.objects.create(
            family_id = family,
        )
        new_post.save()
        return new_post
    
    def update(self, post, data):
        post.content = data.get("content")
        post.emotion = data.get("emotion")
        post.keyword = data.get("keyword")
        post.save()
        return post