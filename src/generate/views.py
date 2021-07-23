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
from .forms import FilesForm

# function to handle an uploaded file.
from .ocr import ocr_file
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files
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
    # form not used
    form = FilesForm(request.POST or None, request.FILES or None)
    context = { 
        # auf DB zugreifen um es dann im html ausgeben zu können
        #"files":files,
        "form": form
    }                 
    return render(request, "index.html", context)

#creating ocr view
def ocr_view(request, *args, **kwargs):
    # foundFile = request.POST.get('fileId') #getting file id from button
    # # print(foundFile)
    # file = Files.objects.get(id=foundFile)
    # ocr_file(file)
    # #updatedFileId = ocr_file(file)
    # #updatedFile = Files.objects.get(id=updatedFileId)
    context = {
        #"foundFile":file,
        #"updatedFile":updatedFile,
    }
    return render(request, "ocr_view.html", context)

# creating table view
def tables_view(request):
    files = Files.objects.all()
    context = { # auf DB zugreifen um es dann im html ausgeben zu können
        "files":files
    }
    return render(request, "tables.html", context)

# creating settings view
def settings_view(request, *args, **kwargs):
    
    return render(request, "settings_view.html", {})

# creating about view
def about_view(request, *args, **kwargs):
    
    return render(request, "about_view.html", {})

# creating login view
def login_view(request, *args, **kwargs):
    
    return render(request, "login.html", {})

# uploaded File can be deleted right away
def delete_file(request, id):
    object = Files.objects.get(id=id)
    object.delete()
    #return render(request,'index.html')
    return redirect('home')

# for saving edited text in ocr_view
def save_changes(request, *args, **kwargs):
    
    #text = request.GET.get('txt')
    #changes = request.POST['changes']
    #print(text)
    #print (changes)
    if request.method == 'POST':
        foundFile = request.POST.get('fileId') #getting file id from button
        # print(foundFile)
        file = Files.objects.get(id=foundFile)
        #if request.POST.get('sms'):
        # do something with text area data since SMS was checked
        changedText = request.POST.get('my_textarea')
        #print(changedText)
        file.ocrtext = changedText
        messages.success(request, 'Changes saved!')
        return render(request, "ocr_view.html", {
        "foundFile":file, # passing ID to template to show and find file again
        #'form': form # for displaying form again
        })
    else:
        messages.warning(request, 'Saving was not successfull, try again!')
        return redirect("ocr_view.html") # wird zurückgeleitet zu home
    # object = Files.objects.get(id=id)
    # object.delete()
    #return render(request,'index.html')
    #return redirect('home')

# Method for displaying all uploaded Files in a List
# class FileView(generic.ListView):
#     model = Files
#     template_name = 'tables.html' # where it's going to be displayed
#     context_object_name = 'tables'
#     paginate_by = 6
#     print (Files.objects.order_by('-id'))

#     def get_queryset(self):
#     	return Files.objects.order_by('-id')

# def uploadForm(request):
# 	# return render(request, 'comment/upload.html') URPSRÜNGLICH
#     return render(request, 'home')

# Method for uploading and saving file to DB, also passing object to template
def uploadFile(request, *args, **kwargs):
    if request.method == 'POST':
        
        form = FilesForm(None, None)
        #if form.is_valid():
        filename = request.POST['filename']
        pdf = request.FILES['pdf']

        a = Files(filename=filename, pdf=pdf, user=request.user)
        a.save()
        # set_globvar(a.filename) # to find name of pdf again
        # set_newid(a.id) # to find id of pdf again
        # path = MEDIA_ROOT + "/pdfs/" + a.filename
        messages.success(request, 'File submitted successfully!')
        # return HttpResponseRedirect(reverse_lazy('home', kwargs={'id': a.id}))
        return render(request, 'index.html', {
            'fileId': a, # passing ID to template to show and find file again
            'form': form # for displaying form again
        })
    else:
    	messages.warning(request, 'Files was not submitted successfully, try again!')
    	return redirect('home') # wird zurückgeleitet zu home


# This is a method to process the OCR-method before loading the ocr_view
def processing(request, *args, **kwargs):
    foundFile = request.POST.get('fileId') #getting file id from button
    # print(foundFile)
    file = Files.objects.get(id=foundFile)
    #messages.info(request, 'Please wait for the OCR to finish!')
    ocr_file(file)
    if file.ocrtext is None:
        messages.warning(request, 'OCR was not successfull, try again!')
        return redirect('home')
    else:
        context = {
                "foundFile":file,
                #"updatedFile":updatedFile,
            }
        return render(request, "ocr_view.html", context)

    #updatedFileId = ocr_file(file)
    #updatedFile = Files.objects.get(id=updatedFileId)
    

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