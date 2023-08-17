from django.shortcuts import render

from files.models import CodeFile


def upload():
    pass


def report():
    pass


def index(request):
    """Главная страница сайта - список файлов."""
    files = CodeFile.objects.all()
    return render(request, 'files/index.html', {'files': files})
