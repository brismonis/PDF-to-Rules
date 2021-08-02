from django.db.models import fields
from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import *
#from django import forms
from django.forms import ModelForm, TextInput, FileInput
  
  
class FilesForm(ModelForm):
    class Meta:
        model = Files
        #fields = "__all__"
        #exclude = ['note', 'rules', 'ocrtext', 'user']
        fields = ['filename', 'pdf', 'authors', 'literature', 'pubyear', 'note']
        widgets = {
            'filename': TextInput(attrs={
                'id':'id-filename',
                'class': "form-control",
                'style': 'max-width: 80%; margin-bottom: 10px;',
                'placeholder': 'Title of File'
                }),
            'pdf': FileInput(attrs={
                'id':'id-pdf',
                'class': "form-control", 
                'style': 'max-width: 80%; margin-bottom: 10px',
                'placeholder': 'PDF File'
                }),
            'authors': TextInput(attrs={
                'id':'id-authors',
                'class': "form-control", 
                'style': 'max-width: 80%; margin-bottom: 10px',
                'placeholder': 'Authors (Optional)'
                }),
            'literature': TextInput(attrs={
                'id':'id-authors',
                'class': "form-control", 
                'style': 'max-width: 80%; margin-bottom: 10px',
                'placeholder': 'Literature (Optional)'
                }),
            'pubyear': TextInput(attrs={
                'id':'id-pubyear',
                'class': "form-control", 
                'style': 'max-width: 80%; margin-bottom: 10px',
                'placeholder': 'Publishing Year (Optional)'
                }),
            'note': Textarea(attrs={
                'id':'id-pubyear',
                'class': "form-control", 
                'style': 'max-width: 80%; max-height:5vw; margin-bottom: 10px',
                'placeholder': 'Notes (Optional)'
                }),
        }