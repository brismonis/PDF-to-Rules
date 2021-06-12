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
 path('', views.homepage_view, name="home"),
 path('upload/', views.uploadFile, name='upload'),

]