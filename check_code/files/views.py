import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from core.decorators import is_author
from files.forms import CodeFileForm
from files.models import CheckCode, CodeFile, FileStatus


@login_required
def upload(request):
    form = CodeFileForm(request.POST or None, request.FILES or None)
    if not form.is_valid():
        return render(request, 'files/upload.html', {'form': form})
    code = form.save(commit=False)
    code.author = request.user
    form.save()
    return redirect('files:index')


@login_required
@is_author
def reupload(request, file_id, **kwargs):
    code = kwargs.get('code', None)
    form = CodeFileForm(
        request.POST or None,
        request.FILES or None,
        instance=code
    )
    if not form.is_valid():
        return render(request, 'files/upload.html', {'form': form})
    path = os.path.join(
        settings.MEDIA_ROOT, f'user_{request.user.id}', code.upload.name)
    if os.path.isfile(path):
        os.remove(path)
    new_code = form.save(commit=False)
    new_code.status = FileStatus.UPDATED
    form.save()
    return redirect('files:index')


@login_required
@is_author
def delete(request, file_id, **kwargs):
    code = kwargs.get('code', None)
    code.upload.delete()
    code.delete()
    return redirect('files:index')


@login_required
@is_author
def reports(request, file_id, **kwargs):
    checks = CheckCode.objects.filter(code_id=file_id).select_related('code')
    return render(request, 'files/reports.html', {'checks': checks})


@login_required
def index(request):
    """Главная страница сайта - список файлов."""
    files = CodeFile.objects.filter(
        author=request.user).prefetch_related('checkcode')
    return render(request, 'files/index.html', {'files': files})
