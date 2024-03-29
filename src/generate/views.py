# Create your views here to handle pages and include html files.
import time, datetime, csv, re
from PyPDF2.generic import PdfObject
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.utils.functional import empty
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pdf2image.pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter

from pdftorules.settings import MEDIA_ROOT, MEDIA_URL # Import TemplateView
from .forms import FilesForm

# function to handle an uploaded file.
from .ocr import ocr_file
from .nlp import nlp_file
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files, Setting
from django.template import RequestContext, context
from django.contrib import messages

from django.db.utils import Error, OperationalError
from django.template import *

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

#creating ocr view
def nlp_view(request, *args, **kwargs):
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
    return render(request, "nlp_view.html", context)

# creating table view
def tables_view(request):
    files = Files.objects.all()
    context = { # auf DB zugreifen um es dann im html ausgeben zu können
        "files":files
    }
    return render(request, "tables.html", context)

# creating settings view
def settings_view(request, *args, **kwargs):
    setting = "English"
    try:
        obj = Setting.objects.get(id=1)
        setting = Setting.get_language(obj)
        print(setting)
    except:
        print("No Settings Object yet")
    
    return render(request, "settings_view.html", {
        "selection":setting, # passing ID to template to show and find file again
        #'form': form # for displaying form again
    })

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

def delete_file_table(request, id):
    object = Files.objects.get(id=id)
    object.delete()
    messages.success(request, 'File "' + object.filename + '" deleted successfully.')
    #return render(request,'index.html')
    return redirect('tables')

def edit_table(request, id):
    file = Files.objects.get(id=id)
    return render(request, "table_edit.html", {
        "fileId":file, # passing ID to template to show and find file again
        #'form': form # for displaying form again
    })


def view_rules(request, id):
    file = Files.objects.get(id=id)
    
    return render(request, "rules_view.html", {
        "foundFile":file, # passing ID to template to show and find file again
        #'form': form # for displaying form again
        })

# Method for saving edited text in ocr_view
def save_changes(request, *args, **kwargs):
    if request.method == 'POST':
        foundFile = request.POST.get('fileId') #getting file id from button
        # print(foundFile)
        file = Files.objects.get(id=foundFile)
        changedText = request.POST.get('my_textarea')
        #print(changedText)
        file.ocrtext = changedText
        file.save()
        messages.success(request, 'Changes saved!')
        return render(request, "ocr_view.html", {
        "foundFile":file, # passing ID to template to show and find file again
        #'form': form # for displaying form again
        })
    else:
        messages.warning(request, 'Saving was not successfull, try again!')
        return redirect("ocr_view.html") # wird zurückgeleitet zu home
    

def save_changes_nlp(request, *args, **kwargs):
    if request.method == 'POST':
        #getting file id and duration from form
        foundFile = request.POST.get('fileId') 
        duration = request.POST.get('duration') 
        file = Files.objects.get(id=foundFile)

        new_rules = request.POST.getlist('value')

        file.ruleslist = new_rules
        file.save()
        
        messages.success(request, 'Changes saved!')
        return render(request, "nlp_view.html", {
        "foundFile":file, # passing ID to template to show and find file again
        "duration": duration,
        })
    else:
        messages.warning(request, 'Saving was not successfull, try again!')
        return redirect("nlp_view.html") # wird zurückgeleitet zu home

def save_changes_table(request, *args, **kwargs):
    if request.method == 'POST':
        #getting file id from form
        foundFile = request.POST.get('fileId') 
        file = Files.objects.get(id=foundFile)
        att = request.POST.getlist('tableedit')
        #print(att)
        file.filename = att[0]
        file.authors = att[1]
        file.literature = att[2]
        file.pubyear = att[3]
        file.note = att[4]


        file.save()
        messages.success(request, 'Changes saved!')
        return redirect('edit_table', id=file.id)
        # return render(request, "rules_view.html", {
        # "foundFile":file, # passing ID to template to show and find file again
        # })
    else:
        messages.warning(request, 'Saving was not successfull, try again!')
        return redirect("table_edit.html") # wird zurückgeleitet


def save_changes_rules(request, *args, **kwargs):
    if request.method == 'POST':
        #getting file id from form
        foundFile = request.POST.get('fileId') 
        file = Files.objects.get(id=foundFile)

        new_rules = request.POST.getlist('value')
        #print(new_rules)
        file.ruleslist = new_rules
        # file.save()
        
        # changedText = request.POST.get('my_textarea')
        # print(changedText)
        # file.rules = changedText
        file.save()
        messages.success(request, 'Changes saved!')
        return redirect('view_rules', id=file.id)
        # return render(request, "rules_view.html", {
        # "foundFile":file, # passing ID to template to show and find file again
        # })
    else:
        messages.warning(request, 'Saving was not successfull, try again!')
        return redirect("rules_view.html") # wird zurückgeleitet zu home

# def split_PDF(pdf, fr, to):
#     fr = int(fr)
#     to = int(to)
#     pdf_input = PdfFileReader(pdf)
#     #pdf_output = PdfFileWriter()
#     page_count = pdf_input.getNumPages()
#     #print (page_count)
#     if (page_count >= fr or page_count >= to or fr < to):
#         #now split pdf by given range
#         pdf_output = PdfFileWriter # Example a PDF file writer
#         for i in range(fr, to):
#             print(i)
#             pdf_output.addPage(pdf_input.getPage(i)) 
#         with open(pdf, "wb") as outputStream:
#             pdf_output.write(outputStream)
#         outputStream.close()
#         return pdf_output
#     else:

#         return 0    


# Method for uploading and saving file to DB, also passing object to template
def uploadFile(request, *args, **kwargs):
    if request.method == 'POST':
        
        form = FilesForm(None, None)
        #if form.is_valid():
        filename = request.POST['filename']
        pdf = request.FILES['pdf']
        authors = request.POST['authors']
        literature = request.POST['literature']
        pubyear = request.POST['pubyear']
        note = request.POST['note']
        from_page = request.POST.get('from')
        to_page = request.POST.get('to')

        a = Files(filename=filename, pdf=pdf, user=request.user, authors=authors, literature=literature, pubyear=pubyear, note=note)
        #print(a.get_pdfpath)
        a.save()

        #pdf_ranged = split_PDF(a.pdf, from_page, to_page)
        #set_globvar(a.filename) # to find name of pdf again
        # set_newid(a.id) # to find id of pdf again
        # path = MEDIA_ROOT + "/pdfs/" + a.filename
        messages.success(request, 'File submitted successfully!')
        # return HttpResponseRedirect(reverse_lazy('home', kwargs={'id': a.id}))
        return render(request, 'index.html', {
            'fileId': a, # passing ID to template to show and find file again
            'form': form, # for displaying form again
            'from_page': from_page,
            'to_page': to_page,
        })

    else:
    	messages.warning(request, 'Files was not submitted successfully, try again!')
    	return redirect('home') # wird zurückgeleitet zu home


# This is a method to process the OCR-method before loading the ocr_view
def processing_ocr(request, *args, **kwargs):
    foundFile = request.POST.get('fileId') #getting file id from button
    from_page = request.POST.get('from')
    to_page = request.POST.get('to')
    if(from_page == '' or to_page == ''):
        from_page = None
        to_page = None

    # print(foundFile)
    file = Files.objects.get(id=foundFile)
    #messages.info(request, 'Please wait for the OCR to finish!')
    start_time = time.time()
    ocr_file(file, from_page, to_page)
    duration = time.time() - start_time
    ty_res = time.gmtime(duration)
    minutes = time.strftime("%M minutes and %S seconds",ty_res)
    #print(minutes)
    if file.ocrtext is None:
        messages.warning(request, 'OCR was not successfull, try again!')
        return redirect('home')
    else:
        context = {
                "foundFile":file,
                #"updatedFile":updatedFile,
            }
        return render(request, "ocr_view.html", context)

def processing_nlp(request, *args, **kwargs):
    foundFile = request.POST.get('fileId') #getting file id from button
    file = Files.objects.get(id=foundFile)
    #all_statements = []
    start_time = time.time()
    nlp_file(file)
    duration = time.time() - start_time
    # duration = duration / 60
    # minutes = round(duration, 2)
    ty_res = time.gmtime(duration)
    minutes = time.strftime("%M minutes and %S seconds",ty_res)
    #minutes = str(datetime.timedelta(seconds=duration))
    #print(minutes)
    if file.rules is None:
        messages.warning(request, 'No Rules found!')
        return redirect('home')
    else:
        context = {
                "foundFile":file,
                "duration": minutes,
                # "my_json":{i: i for i in range(100)},
                #"updatedFile":updatedFile,
            }
        return render(request, "nlp_view.html", context)
    # if file.rules is None:
    #     messages.warning(request, 'No rules found!')
    #     return redirect('home')
    # else:
    #     context = {
    #             "foundFile":file,
    #             #"updatedFile":updatedFile,
    #         }
    #     return render(request, "nlp_view.html", context)


def download_ocr(request, id):
   # some code
   if request.method == "POST":
        if request.POST['request_name'] == 'download_ocr':
            file_data = "some text"
            response = HttpResponse(content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="output.txt"'
            return response
   
# def download(request, id):
#     object = Files.objects.get(id=id)
#     #file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404

# Method for downloading generated rules as csv file
def download_csv(request):
    foundFile = request.POST.get('fileId')
    file = Files.objects.get(id=foundFile)
    
    # Create the HttpResponse object with the appropriate CSV header.
    filename = file.filename
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename='+ filename +'_Netzwerkregeln.csv'},
    )
    
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    # Write a first row with header information
    writer.writerow(["Rules in " + file.filename])
    for i in file.ruleslist:
        #print(i)
        writer.writerow([i])

    return response

def save_language(request):
    selection = request.POST.get('selection') 
    #print(selection)
    if(Setting.objects.filter(id=1).first() is None):
        setting = Setting(default_language=selection)
        setting.save()
        #print("case 1")
    else:
        newsetting = Setting.objects.get(id=1)
        Setting.set_language(newsetting, selection)
        newsetting.save()
        #print("case 2")

    messages.success(request, 'Changes saved!')
        # return HttpResponseRedirect(reverse_lazy('home', kwargs={'id': a.id}))
    return render(request, 'settings_view.html', {
        'selection': selection, # passing ID to template to show and find file again
    })