from django.conf.urls import url

from .views import PhotoUpload, LoadURLView, download_photo


urlpatterns = [
    url(r'upload', PhotoUpload.as_view()),
    url(r'load', LoadURLView.as_view()),
    url(r'download/(?P<pk>[^/]+)$', download_photo, name='download')
]