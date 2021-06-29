import os
from django.db import models
from django.utils.timezone import now
#from datetime import datetime

# Create your models here.
# Komponenten auf einer Seite 
# class pdfs(models.Model):
#     title = models.TextField()
#     pagerange = models.TextField()
#     language = models.TextField()

# class Upload(models.Model):
#     upload_file = models.FileField(upload_to='media/') # speichert einen File in der DB  
#     # upload_date = models.DateTimeField(auto_now_add =True)

class Files(models.Model):
    filename = models.CharField(max_length=500)
    authors = models.CharField(blank=True, null=True, max_length=500)
    literature = models.CharField(blank=True, null=True, max_length=500)
    pubyear = models.CharField(blank=True, null=True, max_length=500)
    user = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateTimeField(default=now, editable=False, blank=True)
    note = models.CharField(blank=True, null=True, max_length=500)
    pdf = models.FileField(upload_to='pdfs/')
    ocrtext = models.TextField(blank=True, null=True) # TextField is for larger strings

    def get_filename(self):
        return self.filename

    def get_pdfpath(self):
        return os.path.basename(self.pdf.path)

    def get_ocrtext(self):
        return self.ocrtext
        
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.filename.delete()
        self.ocrtext.delete()
        self.authors.delete()
        self.literature.delete()
        self.pubyear.delete()
        self.user.delete()
        self.date.delete()
        self.note.delete()
        super().delete(*args, **kwargs)