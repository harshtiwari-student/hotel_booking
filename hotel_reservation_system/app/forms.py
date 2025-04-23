from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "roomid",
            "userid",
            "roomtype",
            "description",
            "price_per_night",
            "image",
            "is_available",
        ]
