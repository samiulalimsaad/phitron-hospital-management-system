import os

import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.views.generic.edit import FormView

from .forms import AppointmentForm, DoctorForm, ReviewForm, UserRegistrationForm
from .models import Appointment, Doctor, Review


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_doctors"] = Doctor.objects.all()[:3]
        context["doctors"] = Doctor.objects.all()
        context["reviews"] = Review.objects.all()
        return context


def verification_failed(request):
    return render(request, "verification_failed.html")


def verify_email(request):
    User = get_user_model()
    print("1")
    if request.method == "GET":
        print("2")
        try:
            # Extract user ID and token from URL parameters
            user_id = request.GET.get("uid")
            print("3", user_id)
            id = int(user_id)
            print("3", id)
            token = request.GET.get("token")
            print("4")

            # Retrieve user object
            user = User.objects.get(pk=id)
            print("5")

            print("inside get", user)
            # Verify the token

            print("6")
            print("inside get")
            # Mark the user as active
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your email has been verified successfully. You can now log in.",
            )
            return redirect("login")

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(e)
            messages.error(request, "Invalid verification link.")

    # Redirect to a failure page or display an error message
    return redirect("verification_failed")


class RegisterView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Save the user without marking them as active
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Generate verification token
        token = default_token_generator.make_token(user)
        print("Verification token generated for user ", (user.id))

        # Construct verification URL
        current_site = get_current_site(self.request)
        verification_url = (
            f"http://{current_site.domain}/verify-email/?uid={user.id}&token={token}"
        )

        # Send verification email
        send_mail(
            "Verify Your Email",
            render_to_string(
                "emails/verification_email.html", {"verification_url": verification_url}
            ),
            "no-reply@hospital.com",
            [user.email],
            fail_silently=False,
        )

        # Display success message
        messages.success(
            self.request,
            "Account created successfully. Check your email for a verification link.",
        )

        # Redirect to the login page
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


class BookAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "home.html"
    success_url = reverse_lazy("+")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()

        return context

    def form_valid(self, form):
        form.instance.doctor_id = self.kwargs["doctor_id"]
        form.instance.patient = self.request.user
        print({"doctor_id": form.instance.doctor_id, "patient": form.instance.patient})
        return super().form_valid(form)


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
