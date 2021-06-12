from django.contrib import admin

# Register your models here.
# Klassen importieren von models
from generate import models

admin.site.register(models.Files)
# admin.site.register(models.pdfs)