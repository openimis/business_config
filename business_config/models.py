from django.db import models

from core.models import HistoryBusinessModel


class BusinessConfig(HistoryBusinessModel):
    key = models.TextField(max_length=255, null=False, blank=False)
    value = models.TextField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
