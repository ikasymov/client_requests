from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=250)
    position = models.CharField(max_length=400)
