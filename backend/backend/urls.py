from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('events/', include("events.urls")),
    path('posts/', include("conversation.urls")),
]