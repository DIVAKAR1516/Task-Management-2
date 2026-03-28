from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# 🔹 Generate JWT
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

# 🔹 SIGNUP
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# 🔹 SIGNUP
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # 📧 Send Welcome Email
        send_mail(
            subject="Welcome to TaskManager",
            message=f"Hi {user.username}, welcome to TaskManager!",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response({
            "message": "User created successfully"
        })

    return Response(serializer.errors, status=400)

# 🔹 LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        tokens = get_tokens(user)

        # 📧 Login Email
        send_mail(
            subject="Login Alert",
            message=f"Hi {user.username}, you logged in successfully.",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response(tokens)

    return Response({"error": "Invalid credentials"}, status=401)