from django.urls import path
from .views import DeviceListView, DeviceDetailView

urlpatterns = [
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('devices/<str:manufacturer_id>/<str:device_id>', DeviceDetailView.as_view(), name='device-detail'),
]
