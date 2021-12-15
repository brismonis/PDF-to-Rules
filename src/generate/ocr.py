import os, re
import pytesseract

from pdftorules.settings import MEDIA_ROOT
# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files, Setting
from pdf2image import convert_from_path
from PIL import Image
# Exception Handling
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError, 
    PDFSyntaxError
)

# more efficient method
def ocr_file(f, fr, to):
    #print (fr)
    PDF_file = Files.get_filename(f)
    JPG_path = os.path.join(MEDIA_ROOT, 'jpgs') # path to jpgs Folder
    path_pdf = Files.get_pdfpath(f)
    PDF_folder = os.path.join(MEDIA_ROOT, 'pdfs') # path to pdfs Folder
    PDF_path = os.path.join(PDF_folder, path_pdf) # path to current object's PDF
    ocred_text = ''
    jpg_paths = []
    language = "eng"
    try:
        obj = Setting.objects.get(id=1)
        setting = Setting.get_language(obj)
        if(setting == "English"):
            language = "eng"
        else:
            language = "deu"
    except:
        print("No Settings Object yet, default language English will be used.")

    # configuration of ocr method
    # https://github.com/madmaze/pytesseract/issues/141
    
    conf = '--oem 3 --psm 1 -c load_system_dawg=0 load_freq_dawg=0 load_punc_dawg=0'
    dpi = 400
    fmt = "jpeg"
    
    try:
        if fr is not None and to is not None:
            fr = int(fr)
            to = int(to)
            # Store all the pages of the PDF in a variable
            pages = convert_from_path(PDF_path, dpi=dpi,fmt=fmt, output_file=PDF_file, output_folder=JPG_path, paths_only=True, first_page=fr, last_page=to, grayscale=True)
            # save paths of converted jpgs to jpg_paths
            jpg_paths = pages
            #print(jpg_paths)
        else:
            # Store all the pages of the PDF in a variable
            pages = convert_from_path(PDF_path, dpi=dpi,fmt=fmt, output_file=PDF_file, output_folder=JPG_path, paths_only=True, grayscale=True)
            # save paths of converted jpgs to jpg_paths
            jpg_paths = pages
    except PDFPageCountError:
        #An invalid PDF file path or a malformed or invalid PDF
        print("An invalid PDF file path or a malformed or invalid PDF.")
    except PDFInfoNotInstalledError:
        print("Exception raised when pdfinfo, which is part of poppler-utils, was not found on your system.")
    except PDFSyntaxError:
        print("Exception raised when convert_from_path or convert_from_bytes is called using strict=True and the input PDF contained a syntax error. Simply use strict=False will usually solve this issue.")
    
    # IMAGE COUNTER useful for progress bar etc.
    # image_counter = 1
    # for page in pages:
    #     image_counter = image_counter + 1

    #print (image_counter)
    #file_limit = image_counter - 1
    #f = open(outfile, "a")

    for jp in jpg_paths:
        #print(jp)
        text = str(((pytesseract.image_to_string(Image.open(jp), lang=language, config=conf))))
        # to remove hyphenation by hyphen
        text = text.replace("-\n", '')
        ocred_text = ocred_text + text
        #f.write(text)
        # remove jpegs after ocr process
        os.remove(jp)

    # for replacing multiple line breaks
    word = re.sub(r'\n+', '\n', ocred_text).strip()
    
    # save to database
    f.ocrtext = word
    #print (f.ocrtext)
    f.save()


# OLD METHOD: less efficient
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