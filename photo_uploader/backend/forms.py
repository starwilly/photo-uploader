from django import forms

from .models import Photo


class PhotoUploadForm(forms.ModelForm):
    ''' photo upload form'''

    class Meta:
        model = Photo
        fields = ['title', 'file']


class ImageURLLoadForm(forms.Form):
    url = forms.URLField(required=True, error_messages={
        'required': 'Please enter a valid image URL'
    })
