from django.conf.urls import url

from .views import PhotoUpload, LoadURLView


urlpatterns = [
    url(r'upload', PhotoUpload.as_view()),
    url(r'load-url', LoadURLView.as_view())
]