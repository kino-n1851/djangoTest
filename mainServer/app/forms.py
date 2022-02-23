from django import forms
from .models import ImageStorage, NumberImage

class StorageForm(forms.ModelForm):
    class Meta:
        model = ImageStorage
        fields = '__all__'

class ImageForm(forms.ModelForm):
    class Meta:
        model = NumberImage
        fields = '__all__'