# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from .forms import PhotoUploadForm


class PhotoUpload(View):
    '''Photo upload view'''

    def post(self, request, *args, **kwargs):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse(data={'success': 'Photo Uploaded'})
