import os, json
from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone
from .validators import validate_file_extension
from django.core.validators import FileExtensionValidator
from pdftorules.settings import MEDIA_ROOT
from django.contrib.postgres.fields import ArrayField

class Setting(models.Model):
    default_language = models.CharField(max_length=20, default="eng")

    def get_language(self):
        return self.default_language
    def set_language(self, txt):
        self.default_language = txt
        #return self.default_language


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

    stm = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)
    rules = models.TextField(blank=True, null=True)

    stmlist = ArrayField(
        models.TextField(blank=True, default=list), 
        blank=True, 
        null = True,
        
    )

    evlist = ArrayField(
        models.TextField(blank=True, default=list), 
        blank=True, 
        null = True,
        
    )

    ruleslist = ArrayField(
        models.TextField(blank=True, default=list), 
        blank=True, 
        null = True,
        
    )


    def get_filename(self):
        return self.filename

    def get_pdfpath(self):
        return os.path.basename(self.pdf.path)

    def get_ocrtext(self):
        return self.ocrtext

    def set_evidence(self, x):
        self.evidence = json.dumps(x)

    def get_evidence(self):
        return json.loads(self.evidence)
        
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
        BN_folder = os.path.join(MEDIA_ROOT, 'boolean_network') # path to bn Folder
        JSON_folder = os.path.join(MEDIA_ROOT, 'json') # path to json Folder
        fname = Files.get_filename(self)
        JSON_file = os.path.join(JSON_folder, fname + '_id' + str(self.id) + '_reach.json')
        BN_file = os.path.join(BN_folder, fname + '_id' + str(self.id) + "_boolnet")
        SIF_file = os.path.join(BN_folder, fname + '_id' + str(self.id) + "_sifstring")
        if os.path.exists(PDF_path):
            os.remove(PDF_path)
        if os.path.exists(BN_file):
            os.remove(BN_file)
        if os.path.exists(JSON_file):
            os.remove(JSON_file)
        if os.path.exists(SIF_file):
            os.remove(SIF_file)
        super().delete(*args, **kwargs)