from django.urls import path
from .views import (
    create_post,
    update_post,
    PostViewSet
    )

post_detail = PostViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "delete": "destroy"
})

urlpatterns = [
    path('create/', create_post, name="create-post"),
    path('update/', update_post, name="update-post"),
    path("<int:pk>/", post_detail, name="post-detail"),
]