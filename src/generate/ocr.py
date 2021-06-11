

def handle_uploaded_file(f):
    print(f.name)
    #  Reading file from storage
    # file = default_storage.open(file_name)
    # file_url = default_storage.url(file_name)
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks(): # Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
    #         destination.write(chunk)