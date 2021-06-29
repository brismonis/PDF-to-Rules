# Create your views here.
# to handle pages
# include html files

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.functional import empty
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from pdf2image.pdf2image import convert_from_path

from pdftorules.settings import MEDIA_ROOT, MEDIA_URL # Import TemplateView
# from .forms import UploadFileForm # for Uploading PDF Files

# function to handle an uploaded file.
from .ocr import ocr_file
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files
from .forms import UploadForm
from django.template import RequestContext, context
from django.contrib import messages

from django.db.utils import OperationalError
# format_list = [('', '(all)')]
# geom_type_list = [('', '(all)')]
# try:
#     format_list.extend([(i[0],i[0]) 
#         for i in format.objects.values_list('name')])
#     geom_type_list.extend([(i[0],i[0]) 
#         for i in geom_type_list.objects.values_list('name')])
# except OperationalError:
#     pass  # happens when db doesn't exist yet, views.py should be
#           # importable without this side effect

# creating homepage view
def homepage_view(request, *args, **kwargs):
    #files = Files.objects.all()
    context = { 
        # auf DB zugreifen um es dann im html ausgeben zu können
        #"files":files,
    }                 
    return render(request, "index.html", context)

#creating ocr view
def ocr_view(request, *args, **kwargs):
    # foundFile = request.POST.get('fileId') #getting file id from button
    # print(foundFile)
    #file = Files.objects.get(id=foundFile)
    #     ocr_file(foundFile)
    context = {
        #"foundFile":file
    }
    return render(request, "ocr_view.html", context)

# creating table view
def tables_view(request):
    #files = Files.objects.all()
    context = { # auf DB zugreifen um es dann im html ausgeben zu können
        #"files":files
    }
    return render(request, "tables.html", context)

# creating settings view
def settings_view(request, *args, **kwargs):
    
    return render(request, "settings_view.html", {})

# creating about view
def about_view(request, *args, **kwargs):
    
    return render(request, "about_view.html", {})

# Method for displaying all uploaded Files in a List
# class FileView(generic.ListView):
#     model = Files
#     template_name = 'tables.html' # where it's going to be displayed
#     context_object_name = 'tables'
#     paginate_by = 6
#     print (Files.objects.order_by('-id'))

#     def get_queryset(self):
#     	return Files.objects.order_by('-id')

# Method for displaying freshly uploaded file
# class TempFileView(generic.ListView):
#         template_name = 'index.html'
#         def get_query(self):
#             return Files.objects.filter(id=self.kwargs['id'])

# def uploadForm(request):
# 	# return render(request, 'comment/upload.html') URPSRÜNGLICH
#     return render(request, 'home')

# Method for uploading and saving file to DB, also passing object to template
def uploadFile(request, *args, **kwargs):
    if request.method == 'POST':
        filename = request.POST['filename']
        pdf = request.FILES['pdf']

        a = Files(filename=filename, pdf=pdf)
        a.save()
        # set_globvar(a.filename) # to find name of pdf again
        # set_newid(a.id) # to find id of pdf again
        # path = MEDIA_ROOT + "/pdfs/" + a.filename
        messages.success(request, 'File submitted successfully!')
        # return HttpResponseRedirect(reverse_lazy('home', kwargs={'id': a.id}))
        return render(request, 'index.html', {
            'fileId': a # passing ID to template to show and find file again
        })
    else:
    	messages.error(request, 'Files was not submitted successfully, try again!')
    	return redirect('home') # wird zurückgeleitet zu home

# def myUpload(request):
# 	return render(request, 'comment/myUpload.html') # TODO:

# def savingtempfile(filename):
#     return filename

# def ocrFile(request, *args, **kwargs):
#     # TODO: ruft ocr.py auf 
#     # thisfile = self.get
#     foundFile = request.POST.get('fileId') #getting file id from button
#     fid = foundFile.id
#     print (fid)
#     # foundFile = Files.objects.get(id=fileId)
#     # print(foundFile.filena me)
#     if request.method == 'POST':
#         #file = Files.objects.get(filename=test)
#         #ocr_file(foundFile)
#         return render(request, 'ocr_view.html', {
#             'fileId': fid # passing ID to template to show and find file again
#         })
#         #return redirect('ocr_view')