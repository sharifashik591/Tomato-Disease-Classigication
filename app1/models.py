from django.db import models

# Create your models here.

class Image(models.Model):
    img=models.FileField(upload_to='img/')