# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.urls import reverse_lazy

from .utils import photo_upload_to


class Photo(models.Model):
    """ Photo model """
    uuid = models.CharField(unique=True,
                            default=uuid.uuid4,
                            max_length=32,
                            editable=False)
    title = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to=photo_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def extension(self):
        _, ext = os.path.splitext(self.file.name)
        return ext.lstrip('.')

    @property
    def download_link(self):
        return reverse_lazy('download', kwargs={'uuid':self.uuid})