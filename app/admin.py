from django.contrib import admin

from app.models import Appointment, Doctor, Patient, Review

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Review)
