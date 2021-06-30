from django.db.models import fields
from django.forms import ModelForm
from .models import *
#from django import forms
from django.forms import ModelForm, TextInput, FileInput
  
  
class FilesForm(ModelForm):
    class Meta:
        model = Files
        #fields = "__all__"
        #exclude = ['note', 'rules', 'ocrtext', 'user']
        fields = ['filename', 'pdf']
        widgets = {
            'filename': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px; margin-bottom: 10px',
                'placeholder': 'Title of File'
                }),
            'pdf': FileInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px; margin-bottom: 10px',
                'placeholder': 'PDF File'
                })
        }