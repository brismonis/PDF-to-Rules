# Um OCR anwenden zu können
import os
import pytesseract

from pdftorules.settings import MEDIA_ROOT
# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files
from pdf2image import convert_from_path
from PIL import Image
#Exception Handling
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError, #An invalid PDF file path or a malformed or invalid PDF
    PDFSyntaxError
)

# old
# def ocr_file(f):
    
#     PDF_file = Files.get_filename(f)
#     path_pdf = Files.get_pdfpath(f)
#     JPG_path = os.path.join(MEDIA_ROOT, 'jpgs') # path to jpgs Folder
#     PDF_folder = os.path.join(MEDIA_ROOT, 'pdfs') # path to pdfs Folder
#     PDF_path = os.path.join(PDF_folder, path_pdf) # path to current object's PDF

#     # Store all the pages of the PDF in a variable
#     pages = convert_from_path(PDF_path, 500,fmt='jpg', output_file=PDF_file, output_folder=JPG_path)
#     ocred_text = ''
#     # Iterate through all the pages stored above
#     for page in pages:
#         text = str(((pytesseract.image_to_string(page))))
#         ocred_text = ocred_text + text
    
#     # Um Silbentrennung im Ergebnis zu meiden
#     #ocred_text = text.replace('-\n', '')
#     # Ergebnis in DB speichern
#     f.ocrtext = ocred_text
#     f.save()
    
#     # deleting JPGs after OCR
#     del pages
#     for f in os.listdir(JPG_path):
#         os.remove(os.path.join(JPG_path, f))

# more efficient method
def ocr_file(f):
    
    PDF_file = Files.get_filename(f)
    JPG_path = os.path.join(MEDIA_ROOT, 'jpgs') # path to jpgs Folder
    path_pdf = Files.get_pdfpath(f)
    PDF_folder = os.path.join(MEDIA_ROOT, 'pdfs') # path to pdfs Folder
    PDF_path = os.path.join(PDF_folder, path_pdf) # path to current object's PDF
    ocred_text = ''
    # Store all the pages of the PDF in a variable
    first_page = 0 #TODO: Bereichauswahl im Template
    last_page = 0
    try:
        pages = convert_from_path(PDF_path, 500,fmt='jpg', output_file=PDF_file, output_folder=JPG_path)
    except PDFPageCountError:
        print("An invalid PDF file path or a malformed or invalid PDF.")
    except PDFInfoNotInstalledError:
        print("Exception raised when pdfinfo, which is part of poppler-utils, was not found on your system.")
    except PDFSyntaxError:
        print("Exception raised when convert_from_path or convert_from_bytes is called using strict=True and the input PDF contained a syntax error. Simply use strict=False will usually solve this issue.")
    

    image_counter = 0
    for page in pages:
        image_counter = image_counter + 1
    #print (image_counter)
    #file_limit = image_counter - 1
    #f = open(outfile, "a")

    for i in range(0, image_counter):
        if(i < 10):
            filename = PDF_file+"0001-0"+str(i)+".jpg"
        else:
            filename = PDF_file+"0001-"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(os.path.join(JPG_path, filename))))))
        text = text.replace('-\n', '')
        ocred_text = ocred_text + text
        #f.write(text)
        os.remove(os.path.join(JPG_path, filename))
    
    f.ocrtext = ocred_text
    f.save()