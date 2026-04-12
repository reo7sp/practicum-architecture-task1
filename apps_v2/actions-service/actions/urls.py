from django.urls import path
from .views import ExecuteActionView

urlpatterns = [
    path('devices/<str:manufacturer_id>/<str:device_id>/actions/<str:action_id>', ExecuteActionView.as_view(), name='execute_action'),
]
