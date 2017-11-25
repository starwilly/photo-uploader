# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json

from django.http import JsonResponse, StreamingHttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .forms import PhotoUploadForm


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
        payload = json.loads(request.body)
        url = payload['url']
        res = requests.get(url, stream=True)
        return StreamingHttpResponse(
            (chunk for chunk in res.iter_content(512 * 1024)),
            content_type=res.headers['Content-Type']
        )
