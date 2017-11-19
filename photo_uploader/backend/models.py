# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Photo(models.Model):
    """ Photo model """
    title = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
