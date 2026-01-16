from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "users/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def profile(request):
    return render(request, "users/profile.html")

@login_required
def delete_account(request):
    user = request.user

   
    user.is_active = False
    user.save()

    logout(request)
    return redirect("login")