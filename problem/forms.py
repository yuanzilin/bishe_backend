from django import forms

class submitForm(forms.Form):
    username = forms.CharField(max_length=100)
    problemName = forms.CharField(max_length=100)
    timeout = forms.CharField(max_length=100)
    type = forms.CharField(max_length=100)
    zip_path = forms.CharField(max_length=100)
    settings_path = forms.CharField(max_length=100)
    subtype = forms.CharField(max_length=100)