import os

import requests
from django.contrib import admin

from app.models import Appointment, Doctor, Patient, Review

from .models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_display = ["user", "expertise", "profile_picture"]
    search_fields = ["user__username", "expertise"]

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["profile_picture"]:
            imgbb_api_key = os.getenv("IMGBB")
            profile_picture = form.cleaned_data["profile_picture"]
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={"key": imgbb_api_key},
                files={"image": profile_picture.file},
            )
            print(response.status_code)
            if response.status_code == 200:
                url = response.json()["data"]["url"]
                obj.profile_picture = url
        super().save_model(request, obj, form, change)


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Review)
