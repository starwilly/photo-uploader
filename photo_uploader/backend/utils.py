import os

from django.conf import settings

def photo_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = '{}{}'.format(instance.id, ext)
    return os.path.join(settings.USER_UPLOAD_TO, filename)
