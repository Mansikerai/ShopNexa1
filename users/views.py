from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



def login_page(request):
    return render(request, "users/login.html")


def register_page(request):
    return render(request, "users/register.html")



class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )

        
class UserDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Welcome {request.user.username} to ShopNexa"
        })

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")   

    return render(request, "users/register.html")
    