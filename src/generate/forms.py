from django import forms

# to check if uploaded file is valid
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )