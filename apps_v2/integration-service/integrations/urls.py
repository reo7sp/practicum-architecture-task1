from django.urls import path
from .views import RegisterDeviceView, UnregisterDeviceView

urlpatterns = [
    path('devices/', RegisterDeviceView.as_view(), name='register_device'),
    path('devices/<str:manufacturer_id>/<str:device_id>', UnregisterDeviceView.as_view(), name='unregister_device'),
]
