import os

import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import FormView

from .forms import AppointmentForm, DoctorForm, ReviewForm, UserRegistrationForm
from .models import Doctor, Review


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_doctors"] = Doctor.objects.all()[:3]
        context["doctors"] = Doctor.objects.all()
        context["reviews"] = Review.objects.all()
        return context


class RegisterView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.email = form.cleaned_data.get("email")
        user.is_active = False
        user.save()
        messages.success(
            self.request,
            "Account created successfully. Check your email for verification link.",
        )
        return redirect("login")


class DoctorProfileView(View):
    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(id=doctor_id)
        appointments = doctor.appointments.all()
        return render(
            request,
            "doctor_profile.html",
            {"doctor": doctor, "appointments": appointments},
        )


class BookAppointmentView(View):
    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(id=doctor_id)
        form = AppointmentForm()
        return render(
            request, "book_appointment.html", {"doctor": doctor, "form": form}
        )

    def post(self, request, doctor_id):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor_id = doctor_id
            appointment.patient = request.user
            appointment.save()
            return redirect("appointment_confirmation")
        return render(request, "book_appointment.html", {"form": form})


class SubmitReviewView(View):
    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(id=doctor_id)
        form = ReviewForm()
        return render(request, "submit_review.html", {"doctor": doctor, "form": form})

    def post(self, request, doctor_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = doctor_id
            review.patient = request.user
            review.save()
            return redirect("review_confirmation")
        return render(request, "submit_review.html", {"form": form})


class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "doctor_form.html"
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        imgbb_api_key = os.getenv("IMGBB")
        profile_picture = form.cleaned_data["profile_picture"]
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": imgbb_api_key},
            files={"image": profile_picture.file},
        )
        if response.status_code == 200:
            # Image uploaded successfully
            url = response.json()["data"]["url"]
            # Update doctor's profile picture URL
            form.instance.profile_picture = url
            return super().form_valid(form)
        else:
            # Image upload failed
            return self.form_invalid(form)
