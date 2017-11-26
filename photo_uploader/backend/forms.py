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


class PhotoDownLoadForm(forms.Form):
    w = forms.IntegerField(required=False)
    h = forms.IntegerField(required=False)

    def get_resize_bound(self):
        if not self.is_valid():
            return None
        data = self.cleaned_data
        if data.get('w') and data.get('h'):
            return data['w'], data['h']
        else:
            return None