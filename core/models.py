from django.db import models

# Create your models here.


class Report(models.Model):
    description = models.CharField(max_length=1000)
    solutions = models.CharField(max_length=1000)


class Description(models.Model):
    description = models.CharField(max_length=1000)
