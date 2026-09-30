from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import UserProfile


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")


        # Check email already exists

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect("register")


        # Create user

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )


        # Create user profile

        UserProfile.objects.create(
            user=user,
            phone_number=phone_number
        )


        # Success message

        messages.success(
            request,
            "Registration successful!"
        )


        return redirect("login")


    # Show register page

    return render(
        request,
        "register.html"
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")


        # Authenticate user

        user = authenticate(
            request,
            username=email,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")


        else:

            messages.error(
                request,
                "Invalid email or password."
            )


    # Show login page

    return render(
        request,
        "login.html"
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect("login")


# =========================
# HOME
# =========================

def home(request):

    return render(
        request,
        "home.html"
    )