# Um OCR anwenden zu können
import pytesseract
import pdf2image
# Models importieren um auf Methoden und Datenbankeinträge zuzugreifen
from .models import Files

def ocr_file(f):
    print(f.id)
    # TODO: convert pdf to jpg and save in media/jpgs


    # TODO: ocr jpgs and show text in UI + save to DB
    
    
    #  Reading file from storage
    # file = default_storage.open(file_name)
    # file_url = default_storage.url(file_name)
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks(): # Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
    #         destination.write(chunk)