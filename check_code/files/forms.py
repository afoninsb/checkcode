from django import forms
from files.models import CodeFile


class CodeFileForm(forms.ModelForm):

    class Meta:
        model = CodeFile
        fields = ('upload', 'description')
