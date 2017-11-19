from django.forms import ModelForm

from .models import Photo


class PhotoUploadForm(ModelForm):
    ''' photo upload form'''

    class Meta:
        model = Photo
        fields = ['title', 'file']
