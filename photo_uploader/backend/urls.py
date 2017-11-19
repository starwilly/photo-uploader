from django.conf.urls import url

from .views import PhotoUpload


urlpatterns = [
    url(r'upload/', PhotoUpload.as_view()),
]