from django.db import models

from .client import Client
from .employee import Employee


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    responsible = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="requests"
    )
