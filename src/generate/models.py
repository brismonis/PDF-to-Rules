from django.db import models

# Create your models here.
# Komponenten auf einer Seite 
class pdfs(models.Model):
    title = models.TextField
    pagerange = models.TextField
    language = models.TextField

class Upload(models.Model):
    upload_file = models.FileField()    
    upload_date = models.DateTimeField(auto_now_add =True)