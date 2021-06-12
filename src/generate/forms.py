from django import forms

# to check if uploaded file is valid
class UploadForm(forms.Form):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    docfile = forms.FileField()