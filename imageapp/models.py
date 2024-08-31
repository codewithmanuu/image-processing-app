from django.db import models

# Create your models here.

class RequestObject(models.Model):
    request_id = models.CharField(max_length=50)
    input_file = models.FileField(upload_to="input/")
    output_file = models.FileField(upload_to="output/")
    status = models.CharField(max_length=20, default='pending')