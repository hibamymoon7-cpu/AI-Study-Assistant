
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # Home Page
    path(
        "",
        views.home,
        name="home"
    ),

    # User Registration
    path(
        "register/",
        views.register,
        name="register"
    ),

    # User Login
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    # User Logout
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    # Study Materials Page
    path(
        "study-materials/",
        views.study_materials,
        name="study_materials"
    ),

    # Delete Study Material
    path(
        "study-materials/delete/<int:material_id>/",
        views.delete_study_material,
        name="delete_study_material"
    ),

    # Forgot Password - Send Reset Email
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.txt",
            html_email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset"
    ),

    # Password Reset Email Sent Page
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    # Set New Password Page
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    # Password Changed Successfully Page
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

]
