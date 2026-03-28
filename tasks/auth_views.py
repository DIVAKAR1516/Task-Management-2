from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer


# 🔹 Generate JWT
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


# 🔹 SIGNUP
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        try:
            send_mail(
                subject="Welcome to TaskManager",
                message=f"Hi {user.username}, welcome to TaskManager!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except Exception as e:
            print("Email error:", e)

        return Response({
            "success": True,
            "message": "User created successfully"
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# 🔹 LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({
            "error": "Username and password are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        tokens = get_tokens(user)

        try:
            send_mail(
                subject="Login Alert",
                message=f"Hi {user.username}, you logged in successfully.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except Exception as e:
            print("Email error:", e)

        return Response({
            "success": True,
            "tokens": tokens
        })

    return Response({
        "success": False,
        "error": "Invalid credentials"
    }, status=status.HTTP_401_UNAUTHORIZED)