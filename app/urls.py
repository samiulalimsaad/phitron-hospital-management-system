from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    BookAppointmentView,
    DoctorProfileView,
    RegisterView,
    SubmitReviewView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("doctor/<int:doctor_id>/", DoctorProfileView.as_view(), name="doctor_profile"),
    path(
        "book_appointment/<int:doctor_id>/",
        BookAppointmentView.as_view(),
        name="book_appointment",
    ),
    path(
        "submit_review/<int:doctor_id>/",
        SubmitReviewView.as_view(),
        name="submit_review",
    ),
]
