# Create your views here.
# to handle pages
# include html files

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from pdftorules.settings import MEDIA_ROOT, MEDIA_URL # Import TemplateView
from .forms import UploadFileForm # for Uploading PDF Files

# function to handle an uploaded file.
from .ocr import handle_uploaded_file
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import *


# creating homepage view
def homepage_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello</h1>") # prints Hello in path /home (kann man in urls.py festlegen)
    return render(request, "index.html", {})

# creating table view
def tables_view(request):
    context = { 
        # auf Datenbank zugreifen und dann in html ausgeben lassen
    }
    # return HttpResponse("<h1>Hello</h1>") # prints Hello in path /home (kann man in urls.py festlegen)
    return render(request, "tables.html", {})

# for Uploading PDF Files
def upload_file(request):
    if request.method == 'POST':
        # files are uploaded to request.files
        print("log1")
        uploaded_file = request.FILES['document'] # use that name in html
        handle_uploaded_file(uploaded_file)
        #  Saving POST'ed file to storage
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        print("log2")


        # what to do with it
        # fs = FileSystemStorage
        # fs.save(uploaded_file.name, uploaded_file)
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid(): # checks if uploaded file is valid
    #         # handle_uploaded_file(request.FILES['file']) # method from ocr.py
    #         # return HttpResponseRedirect('/success/url/')
    #         uploaded_file = request.FILES['document']
    #         # what to do with it
    #         fs = FileSystemStorage()
    #         fs.save(uploaded_file.name, uploaded_file)
    # else:
    #     form = UploadFileForm()
    return render(request, 'index.html' )#, {'form': form})