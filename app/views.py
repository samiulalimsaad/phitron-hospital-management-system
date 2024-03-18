from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView

from .forms import AppointmentForm, ReviewForm, UserRegistrationForm
from .models import Doctor


class RegisterView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()  # Reload the user object to access the profile fields
        user.email = form.cleaned_data.get("email")
        user.is_active = False  # Deactivate until email confirmation
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


class BookAppointmentView(FormView):
    template_name = "book_appointment.html"
    form_class = AppointmentForm

    def form_valid(self, form):
        doctor_id = self.kwargs["doctor_id"]
        doctor = Doctor.objects.get(id=doctor_id)
        appointment = form.save(commit=False)
        appointment.doctor = doctor
        appointment.patient = self.request.user.patient
        appointment.save()
        messages.success(self.request, "Appointment booked successfully.")
        return redirect("dashboard")


class SubmitReviewView(FormView):
    template_name = "submit_review.html"
    form_class = ReviewForm

    def form_valid(self, form):
        doctor_id = self.kwargs["doctor_id"]
        doctor = Doctor.objects.get(id=doctor_id)
        review = form.save(commit=False)
        review.doctor = doctor
        review.patient = self.request.user.patient
        review.save()
        messages.success(self.request, "Review submitted successfully.")
        return redirect("dashboard")
