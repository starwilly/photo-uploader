# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
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
