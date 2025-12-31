from django.urls import path
from .views import (
    RegisterAPIView,
    UserDashboardAPIView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="jwt_login"),
    path("dashboard/", UserDashboardAPIView.as_view(), name="jwt_dashboard"),
    path("register/", RegisterAPIView.as_view(), name="jwt_register")

]

