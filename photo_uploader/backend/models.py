# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
from .utils import photo_upload_to

from django.db import models
from django.utils.functional import cached_property
from django.urls import reverse_lazy


class Photo(models.Model):
    """ Photo model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to=photo_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @cached_property
    def extension(self):
        _, ext = os.path.splitext(self.file.name)
        return ext[1:]

    @property
    def download_link(self):
        return reverse_lazy('download', kwargs={'pk':self.pk})