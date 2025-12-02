from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import bcrypt
import jwt
from django.conf import settings
from .models import User, Session
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    LoginResponseSerializer,
    SessionCheckResponseSerializer
)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': timezone.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': timezone.now(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        password_hash = hash_password(password)
        user = User.objects.create(email=email, password_hash=password_hash)

        return Response(status=status.HTTP_200_OK)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        if not verify_password(password, user.password_hash):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        token = generate_token(user.id)

        session = Session.objects.create(
            token=token,
            user=user,
            expires_at=timezone.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        )

        return Response(LoginResponseSerializer({'token': token}).data, status=status.HTTP_200_OK)


class CheckSessionView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'error': 'Invalid authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        user_id = verify_token(token)

        if not user_id:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            session = Session.objects.get(token=token, expires_at__gt=timezone.now())
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(SessionCheckResponseSerializer({'user_id': session.user.id}).data, status=status.HTTP_200_OK)
