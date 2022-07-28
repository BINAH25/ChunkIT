from django.db import models

class File(models.Model):
    file = models.FileField(upload_to="uploads/user-files")
    processed_file = models.FileField(upload_to="uploads/processed-files",null=True,blank=True)
