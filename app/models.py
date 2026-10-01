## Create your models here.

from django.db import models
from django.contrib.auth.models import User


# =========================
# USER PROFILE
# =========================

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


# =========================
# STUDY MATERIAL
# =========================

class StudyMaterial(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    # Extracted text from uploaded PDF
    pdf_text = models.TextField(
        blank=True
    )

    file = models.FileField(
        upload_to="study_materials/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# QUESTION
# =========================

class Question(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question[:50]


# =========================
# MCQ
# =========================

class MCQ(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    material = models.ForeignKey(
        StudyMaterial,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    option_a = models.CharField(
        max_length=255
    )

    option_b = models.CharField(
        max_length=255
    )

    option_c = models.CharField(
        max_length=255
    )

    option_d = models.CharField(
        max_length=255
    )

    correct_answer = models.CharField(
        max_length=1
    )

    def __str__(self):
        return self.question[:50]