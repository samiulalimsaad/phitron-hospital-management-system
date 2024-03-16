from django.contrib.auth.models import User
from django.db import models


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to="doctor_profiles/", null=True, blank=True
    )

    def __str__(self):
        return self.user.get_full_name()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    appointment_date = models.DateTimeField()
    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()}'s appointment with Dr. {self.doctor.user.get_full_name()}"


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.patient.user.get_full_name()} for Dr. {self.doctor.user.get_full_name()}"
