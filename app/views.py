
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from pypdf import PdfReader

from .models import UserProfile, StudyMaterial


# =========================
# HOME
# =========================

def home(request):
    return render(request, "home.html")


# =========================
# REGISTER
# =========================

def register(request):

    if request.user.is_authenticated:
        return redirect("study_materials")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            messages.error(request, "Please fill in all required fields.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "This account already exists.")
            return redirect("register")

        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return redirect("register")

        try:
            with transaction.atomic():

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name
                )

                UserProfile.objects.create(user=user)

            messages.success(
                request,
                "Registration successful! Please login."
            )
            return redirect("login")

        except Exception:
            messages.error(
                request,
                "Registration failed. Please try again."
            )
            return redirect("register")

    return render(request, "register.html")


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("study_materials")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:
            messages.error(
                request,
                "Please enter your email and password."
            )
            return redirect("login")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.GET.get("next")

            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)

            return redirect("study_materials")

        messages.error(
            request,
            "Invalid email or password."
        )

    return render(request, "login.html")


# =========================
# LOGOUT
# =========================

@login_required
def user_logout(request):

    if request.method == "POST":
        logout(request)
        messages.success(
            request,
            "You have been logged out successfully."
        )
        return redirect("login")

    return redirect("study_materials")


# =========================
# STUDY MATERIALS
# =========================

@login_required
def study_materials(request):

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        uploaded_file = request.FILES.get("file")

        if not title:
            messages.error(request, "Please enter a material title.")
            return redirect("study_materials")

        if not uploaded_file:
            messages.error(request, "Please select a PDF file.")
            return redirect("study_materials")

        if not uploaded_file.name.lower().endswith(".pdf"):
            messages.error(request, "Only PDF files are allowed.")
            return redirect("study_materials")

        # Extract text from the PDF
        pdf_text = ""

        try:
            reader = PdfReader(uploaded_file)

            if reader.is_encrypted:
                messages.error(
                    request,
                    "Password-protected PDFs are not supported."
                )
                return redirect("study_materials")

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    pdf_text += page_text + "\n"

            # Reset file position before saving
            uploaded_file.seek(0)

        except Exception:
            messages.error(
                request,
                "Unable to read this PDF. Please select a valid PDF."
            )
            return redirect("study_materials")

        # Save the material for the logged-in user
        try:
            StudyMaterial.objects.create(
                user=request.user,
                title=title,
                description=description,
                pdf_text=pdf_text,
                file=uploaded_file
            )

            messages.success(
                request,
                "Study material uploaded successfully!"
            )

        except Exception:
            messages.error(
                request,
                "Unable to save the material. Please check your model fields."
            )

        return redirect("study_materials")

    materials = StudyMaterial.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "study_materials.html",
        {"materials": materials}
    )


# =========================
# DELETE STUDY MATERIAL
# =========================

@login_required
def delete_study_material(request, material_id):

    if request.method != "POST":
        return redirect("study_materials")

    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        user=request.user
    )

    # Delete the uploaded file
    if material.file:
        material.file.delete(save=False)

    # Delete the database record
    material.delete()

    messages.success(
        request,
        "Study material deleted successfully."
    )

    return redirect("study_materials")
