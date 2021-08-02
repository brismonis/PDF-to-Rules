import os
from django.db import models
from django.utils import timezone
from .validators import validate_file_extension
from django.core.validators import FileExtensionValidator
from pdftorules.settings import MEDIA_ROOT



class Files(models.Model):
    filename = models.CharField(max_length=500)
    authors = models.CharField(blank=True, null=True, max_length=500)
    literature = models.CharField(blank=True, null=True, max_length=500)
    pubyear = models.CharField(blank=True, null=True, max_length=500)
    user = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateTimeField(default=timezone.now, editable=False, blank=True)
    note = models.CharField(blank=True, null=True, max_length=500)
    pdf = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator( ['pdf'] ) ])
    ocrtext = models.TextField(blank=True, null=True) # TextField is for larger strings
    rules = models.TextField(blank=True, null=True)

    def get_filename(self):
        return self.filename

    def get_pdfpath(self):
        return os.path.basename(self.pdf.path)

    def get_ocrtext(self):
        return self.ocrtext
        
    def delete(self, *args, **kwargs):
        # self.pdf.delete()
        # self.filename = None
        # self.ocrtext = None
        # self.authors = None
        # self.literature = None
        # self.pubyear = None
        # self.user = None
        # self.date = None
        # self.note = None
        # self.rules = None
        path_pdf = Files.get_pdfpath(self)
        PDF_folder = os.path.join(MEDIA_ROOT, 'pdfs') # path to pdfs Folder
        PDF_path = os.path.join(PDF_folder, path_pdf) # path to current object's PDF
        if os.path.exists(PDF_path):
            os.remove(PDF_path)
        super().delete(*args, **kwargs)