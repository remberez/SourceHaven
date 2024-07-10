from django import forms


class UploadProjectForm(forms.Form):
    file = forms.FileField()
