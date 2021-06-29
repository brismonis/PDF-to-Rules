# Um OCR anwenden zu können
import os
import pytesseract
import pdf2image

from pdftorules.settings import MEDIA_ROOT
# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files
from pdf2image import convert_from_path

def ocr_file(f):
    
    PDF_file = Files.get_filename(f)
    path_pdf = Files.get_pdfpath(f)
    JPG_path = os.path.join(MEDIA_ROOT, 'jpgs') # path to jpgs Folder
    PDF_folder = os.path.join(MEDIA_ROOT, 'pdfs') # path to pdfs Folder
    PDF_path = os.path.join(PDF_folder, path_pdf) # path to current object's PDF

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_path, 500,fmt='jpg', output_file=PDF_file, output_folder=JPG_path)
    ocred_text = ''
    # Iterate through all the pages stored above
    for page in pages:
        text = str(((pytesseract.image_to_string(page))))
        ocred_text = ocred_text + text

    print (ocred_text)
    #f.ocrtext = ocred_text
    #f.save()

    # deleting JPGs after OCR
    del pages
    for f in os.listdir(JPG_path):
        os.remove(os.path.join(JPG_path, f))

    # TODO: show text in UI + save to DB
    

    #  Reading file from storage
    # file = default_storage.open(file_name)
    # file_url = default_storage.url(file_name)
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks(): # Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
    #         destination.write(chunk)