from django.urls import path
from autogen.apps import AutogenConfig
from .views import ScheduleJsonAPIView, InfoView

app_name = AutogenConfig.name

urlpatterns = [
    path('', InfoView.as_view(), name='info'),
    path('api/get_schedule/', ScheduleJsonAPIView.as_view(), name='get_schedule'),
]