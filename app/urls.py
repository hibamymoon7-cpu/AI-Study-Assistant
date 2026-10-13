
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Home Page
    path("", views.home, name="home"),

    # Register
    path("register/", views.register, name="register"),

    # Login
    path("login/", views.user_login, name="login"),

    # Logout
    path("logout/", views.user_logout, name="logout"),

    # Study Materials
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

    # Forgot Password
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

    # Reset Email Sent
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    # Choose New Password
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete")
        ),
        name="password_reset_confirm"
    ),

    # Password Reset Completed
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]

