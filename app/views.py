from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from pypdf import PdfReader

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

    # =========================
    # PDF UPLOAD
    # =========================

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")

        # Check file
        if not file:

            messages.error(
                request,
                "Please select a PDF file."
            )

            return redirect("study_materials")

        # Check PDF
        if not file.name.lower().endswith(".pdf"):

            messages.error(
                request,
                "Only PDF files are allowed."
            )

            return redirect("study_materials")

        # =========================
        # READ PDF TEXT
        # =========================

        pdf_text = ""

        try:

            reader = PdfReader(file)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    pdf_text += text + "\n"

        except Exception:

            messages.error(
                request,
                "Unable to read this PDF."
            )

            return redirect("study_materials")

        # =========================
        # SAVE STUDY MATERIAL
        # =========================

        StudyMaterial.objects.create(
            user=request.user,
            title=title,
            description=description,
            pdf_text=pdf_text,
            file=file
        )

        messages.success(
            request,
            "PDF uploaded and text extracted successfully!"
        )

        return redirect("study_materials")

    # =========================
    # SHOW USER MATERIALS
    # =========================

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
# =========================
# DELETE STUDY MATERIAL
# =========================

@login_required
def delete_study_material(request, material_id):

    if request.method == "POST":

        material = StudyMaterial.objects.filter(
            id=material_id,
            user=request.user
        ).first()

        if material:

            # Delete uploaded PDF
            if material.file:
                material.file.delete(save=False)

            # Delete database record
            material.delete()

            messages.success(
                request,
                "Study material deleted successfully."
            )

        else:

            messages.error(
                request,
                "Study material not found."
            )

    return redirect("study_materials")