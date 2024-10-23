from django import forms
from .models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'opening_days', 'opening_hours', 'phone', 'image1', 'image2', 'image3', 'location_link']
