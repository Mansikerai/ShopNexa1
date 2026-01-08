from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)   # ✅ SESSION LOGIN
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        User.objects.create_user(username=username, password=password1)
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "users/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")




    