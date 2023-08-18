from django import forms

from files.models import CodeFile


class CodeFileForm(forms.ModelForm):

    class Meta:
        model = CodeFile
        fields = ('upload', 'description')

    def clean_upload(self):
        data = self.cleaned_data['upload']
        ext = data.name.split('.')[-1]
        if ext != 'py':
            raise forms.ValidationError('Можно только .py файлы')
        return data
