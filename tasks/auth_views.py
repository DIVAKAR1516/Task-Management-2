from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import SignupSerializer
from .models import TaskUserProfile

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
        
        # Create TaskUserProfile for the user
        TaskUserProfile.objects.create(user=user)

        try:
            send_mail(
                subject="Welcome to TaskManager",
                message=f"Hi {user.username}, welcome to TaskManager! Your account has been created successfully.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except Exception as e:
            print("Email error:", e)

        # Generate tokens after successful signup
        tokens = get_tokens(user)
        
        return Response({
            "success": True,
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "tokens": tokens
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
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "tokens": tokens
        })

    return Response({
        "success": False,
        "error": "Invalid credentials"
    }, status=status.HTTP_401_UNAUTHORIZED)


# 🔹 LOGOUT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            "success": True,
            "message": "Logout successful"
        })
    except TokenError:
        return Response({
            "success": False,
            "error": "Invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)


# 🔹 GET CURRENT USER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    return Response({
        "success": True,
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        }
    })