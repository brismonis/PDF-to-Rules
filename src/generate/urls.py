from os import get_exec_path, name
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import url, include
from django.views.generic import TemplateView
# nicht sicher was das bringt 
from django.views.generic import RedirectView
# reverse_lazy('name') gibt Pfad und hängt name an
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
import re
from . import views

urlpatterns = [
    # path('', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False), name='root'),
    # path('admin/', admin.site.urls),
    # path('generate/', views.homepage_view, name='generate'), # index.html
    # path('generate/tables/', views.tables_view, name='tables'), # (?P<path>.*)$
    # re_path('tables/', views.tables_view),
    # url(r'^tables/$', TemplateView.as_view(tables_view), name='tables'),
    
]

urlpatterns = [
 path('', views.homepage_view, name="home"), #links to homepage
 path('upload/', views.uploadFile, name='upload'), #links to uploadFile method
 #path('processing/', views.ocrFile, name='ocr'), #links to ocr method
 path('ocr-view/', views.ocr_view, name='ocr_view'), #links to ocr View
 path('ocr/', views.processing_ocr, name='processingOcr'), #links to ocr method
 path('delete/<int:id>', views.delete_file, name='delete'), #deleting file after upload
 path('delete_table/<int:id>', views.delete_file_table, name='delete_table'), #deleting file after upload
 path('ocr/saved/', views.save_changes, name='save'),
 path('nlp-view/', views.nlp_view, name='nlp_view'),
 path('nlp/', views.processing_nlp, name='processingNlp'),

 
 #url(r'^(?P<brand>\w+)/$', , name = 'tempfile_view'),
 #re_path(r'^(?P<id>\d+)/?$', views.TempFileView, name='tempfile_view'),
]