from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    BookAppointmentView,
    DoctorProfileView,
    DoctorUpdateView,
    HomePageView,
    RegisterView,
    SubmitReviewView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
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
    path("update/<int:pk>/", DoctorUpdateView.as_view(), name="doctor_update"),
]
