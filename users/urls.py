from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),

    path("profile/", views.profile, name="profile"),
    path("addresses/", views.addresses, name="addresses"),
    
    path("addresses/edit/<int:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<int:id>/", views.delete_address, name="delete_address"),

    path("logout/", views.logout_view, name="logout"),
    path("delete-account/", views.delete_account, name="delete_account"),
]
