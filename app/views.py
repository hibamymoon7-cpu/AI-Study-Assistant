from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, StudyMaterial


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")

        # Check email
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
            user=user
        )

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("login")

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

            login(request, user)

            # Login successful → Study Materials
            return redirect("study_materials")

        else:

            messages.error(
                request,
                "Invalid email or password."
            )

    return render(
        request,
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@login_required
def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    # Logout → Login page
    return redirect("login")


# =========================
# HOME
# =========================

def home(request):

    return render(
        request,
        "home.html"
    )


# =========================
# STUDY MATERIALS
# =========================

@login_required
def study_materials(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")

        # Check file
        if not file:

            messages.error(
                request,
                "Please select a file."
            )

            return redirect("study_materials")

        # Save study material
        StudyMaterial.objects.create(
            user=request.user,
            title=title,
            description=description,
            file=file
        )

        messages.success(
            request,
            "Study material uploaded successfully!"
        )

        return redirect("study_materials")

    # Show only logged-in user's materials
    materials = StudyMaterial.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "study_materials.html",
        {
            "materials": materials
        }
    )