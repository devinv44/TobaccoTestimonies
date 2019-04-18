from django.db import models

# Create your models here.

class Query(models.Model):
    name = models.CharField(max_length = 250, default="Devin") 
