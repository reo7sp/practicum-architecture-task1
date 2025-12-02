from django.urls import path
from .views import RegisterUserView, LoginUserView, CheckSessionView

urlpatterns = [
    path('users/', RegisterUserView.as_view(), name='register_user'),
    path('sessions/', LoginUserView.as_view(), name='login_user'),
    path('sessions/check', CheckSessionView.as_view(), name='check_session'),
]
