# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from easy_thumbnails.files import get_thumbnailer

from django.core.exceptions import ValidationError
from django.http import JsonResponse, StreamingHttpResponse, FileResponse, Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from .forms import PhotoUploadForm, ImageURLLoadForm, PhotoDownLoadForm
from .models import Photo


@method_decorator(csrf_exempt, name='dispatch')
class PhotoUpload(View):
    '''Photo upload view'''

    def post(self, request, *args, **kwargs):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse(data={'success': 'Photo Uploaded'})
        else:
            return JsonResponse(status=400, data={'error': form.errors})


@method_decorator(csrf_exempt, name='dispatch')
class LoadURLView(View):
    def post(self, request, *args, **kwargs):
        form = ImageURLLoadForm(json.loads(request.body))
        if not form.is_valid():
            return JsonResponse(status=400, data={'error': form.errors})
        url = form.cleaned_data['url']
        res = requests.get(url, stream=True)
        return StreamingHttpResponse(
            (chunk for chunk in res.iter_content(512 * 1024)),
            content_type=res.headers['Content-Type']
        )


def download_photo(request, pk):
    """ generate thumbnail """
    try:
        photo = get_object_or_404(Photo, pk=pk)
    except ValidationError:
        raise Http404

    form = PhotoDownLoadForm(request.GET)
    resize_bound = form.get_resize_bound()
    if resize_bound:
        thumbnailer = get_thumbnailer(photo.file.name)
        options = {'crop': True, 'size': resize_bound}
        file = thumbnailer.generate_thumbnail(options)
    else:
        file = photo.file
    return FileResponse(file, content_type='image/' + photo.extension)
