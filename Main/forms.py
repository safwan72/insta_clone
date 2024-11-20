from django import forms
from . import models



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=models.Story
        fields = ['story']