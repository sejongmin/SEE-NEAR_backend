from django.urls import path, register_converter
from .views import (create_event, get_event)
from .converters import DateConverter

register_converter(DateConverter, "date")

urlpatterns = [
    path('create-event/', create_event),
    path('get-events/<date:date>/', get_event),
]