from django import forms
from .models import CategoryImage

class ImageForm(forms.ModelForm):
    class Meta:
        model =CategoryImage
        fields = ('image',)
        