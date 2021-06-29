import os
from django.db import models

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
    filename = models.CharField(max_length=100)
    # owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')
    ocrtext = models.CharField(blank=True, null=True)

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
        super().delete(*args, **kwargs)