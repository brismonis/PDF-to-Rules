from django.contrib import admin

# Register your models here.
# Klassen importieren von models
from .models import Files

admin.site.register(Files)
# admin.site.register(models.pdfs)