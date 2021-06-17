# Create your views here.
# to handle pages
# include html files

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView

from pdftorules.settings import MEDIA_ROOT, MEDIA_URL # Import TemplateView
# from .forms import UploadFileForm # for Uploading PDF Files

# function to handle an uploaded file.
from generate.ocr import ocr_file
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files
from .forms import UploadForm
from django.template import RequestContext
from django.contrib import messages


# creating homepage view
def homepage_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello</h1>") # prints Hello in path /home (kann man in urls.py festlegen)
    return render(request, "index.html", {})

def ocr_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello</h1>") # prints Hello in path /home (kann man in urls.py festlegen)
    return render(request, "ocr_view.html", {})

# creating table view
def tables_view(request):
    context = { 
        # auf Datenbank zugreifen und dann in html ausgeben lassen
    }
    # return HttpResponse("<h1>Hello</h1>") # prints Hello in path /home (kann man in urls.py festlegen)
    return render(request, "tables.html", {})

# Method for displaying all uploaded Files in a List
# class FileView(generic.ListView):
#     model = Files
#     template_name = 'table.html' # where it's going to be displayed
#     context_object_name = 'files'
#     paginate_by = 6

#     def get_queryset(self):
#     	return Files.objects.order_by('-id')

def uploadForm(request):
	# return render(request, 'comment/upload.html') URPSRÜNGLICH
    return render(request, 'home')

def uploadFile(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        pdf = request.FILES['pdf']

        a = Files(filename=filename, pdf=pdf)
        a.save()
        messages.success(request, 'File submitted successfully!')
        return redirect('home') # TODO: weiterleiten 
    else:
    	messages.error(request, 'Files was not submitted successfully, try again!')
    	return redirect('home') # wird zurückgeleitet zu home

def myUpload(request):
	return render(request, 'comment/myUpload.html') # TODO:

def ocrFile(request):
    # TODO: ruft ocr.py auf 
    if request.method == 'POST':
        #file = Files.objects.get()
        return redirect('ocr_view')




# def model_form_upload(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             print (form.errors)
#             instance = UploadForm(request.FILES['myfile'])
#             instance.save()
#             return HttpResponseRedirect('home')
#     else:
#         form = UploadForm()
#     return render(request, 'index.html', {'form': form})

# # def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         # form = UploadFileForm(request.POST, request.FILES)
#         # if form.is_valid():
#         newdoc = Upload(docfile = request.FILES['docfile'])
#         newdoc.save()

#             # Redirect to the document list after POST
#             # return HttpResponseRedirect(reverse('generate.views.index'))
#     # else:
#     #     form = UploadFileForm() # A empty, unbound form

#     # Load documents for the list page
#     documents = Upload.objects.all()

#     # Render list page with the documents and the form
#     return render(
#         'index.html',
#         {'documents': documents},
#         context_instance=RequestContext(request)
#     )


# for Uploading PDF Files
# def upload_file(request):

    # if request.method == 'POST':
    #     # files are uploaded to request.files

    #     print("log1")
    #     uploaded_file = Upload(request.FILES['document']) # use that name in html
    #     uploaded_file.save
    #     documents = Upload.objects.all()
    #     # handle_uploaded_file(uploaded_file)
    #     #  Saving POST'ed file to storage
    #     # file_name = default_storage.save(uploaded_file.name, uploaded_file)
    #     print("log2")

        # model = Upload
        # fields = ['upload_file']
        # success_url = reverse_lazy('fileupload')
        # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['documents'] = Upload.objects.all()
        # return context


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
    # return render(request, 'index.html' )#, {'form': form})