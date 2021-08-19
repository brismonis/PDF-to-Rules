"""pdftorules URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

# import your views
# from generate.views import homepage_view, tables_view # , next_view usw
# from generate.views import tables_view
from generate import views

# urlpatterns = patterns('',
#         (r'^upload/', include('upload.urls')),
#         (r'^$', 'upload.views.index'),
#         (r'^admin/', include(admin.site.urls)),) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     # url(re('^admin/'), admin.site.urls),
#     path('admin/', admin.site.urls),
#     path('generate/', views.homepage_view, name='generate')
#     # url('generate/', include(generate.site.urls, namespace='generate'))

# ]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('comment.urls')),
# ]

urlpatterns = [
    # Key difference between path and re_path is that path uses route without regex
    # You can use re_path for complex regex calls and use just path for simpler lookups
    
    #path('', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False), name='root'), # ohne Path leitet es zur admin Seite
    path('admin/', admin.site.urls, name='admin'),
    path('', include('generate.urls')),
    #path('home/', views.homepage_view, name='home'), # index.html
    path('tables/', views.tables_view, name='tables'), # (?P<path>.*)$
    path('tables/rules/<int:id>', views.view_rules, name='view_rules'),
    path('tables/rules/saved', views.save_changes_rules, name='save_rules'),
    path('tables/edit/<int:id>', views.edit_table, name='edit_table'),
    path('tables/edit/saved', views.save_changes_table, name='save_table'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    # re_path(r'^tables/', views.tables_view, name='tables'),
    # re_path('tables/', views.tables_view),
    # url(r'^tables/$', TemplateView.as_view(tables_view), name='tables'),
    
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# serving Django Media Files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

