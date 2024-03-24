from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Appointment, Doctor, Review


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_date"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["expertise", "profile_picture"]
