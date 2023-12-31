import os

import redis
from core.decorators import is_author
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from files.forms import CodeFileForm
from files.models import CheckCode, CodeFile, FileStatus

r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


@login_required
def upload(request):
    """Загрузка файла с кодом."""
    form = CodeFileForm(request.POST or None, request.FILES or None)
    if not form.is_valid():
        return render(request, 'files/upload.html', {'form': form})
    code = form.save(commit=False)
    code.author = request.user
    form.save()
    path = os.path.join(settings.MEDIA_ROOT, code.upload.name)
    data = (
        f'{code.id}:{path}:{code.upload.name.split("/")[-1]}:'
        f'{request.user.email}'
    )
    r.lpush('to_check', data)
    return redirect('files:index')


@login_required
@is_author
def reupload(request, file_id, **kwargs):
    """Обновление файла с кодом."""
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
    path = os.path.join(settings.MEDIA_ROOT, new_code.upload.name)
    data = (
        f'{new_code.id}:{path}:{new_code.upload.name.split("/")[-1]}:'
        f'{request.user.email}'
    )
    r.lpush('to_check', data)
    return redirect('files:index')


@login_required
@is_author
def delete(request, file_id, **kwargs):
    """Удаление файла."""
    code = kwargs.get('code', None)
    code.upload.delete()
    code.delete()
    return redirect('files:index')


@login_required
@is_author
def reports(request, file_id, **kwargs):
    """Отчёты об анализе кода в файле."""
    checks = CheckCode.objects.filter(code_id=file_id).select_related('code')
    return render(request, 'files/reports.html', {'checks': checks})


@login_required
def index(request):
    """Главная страница сайта - список файлов пользователя."""
    files = CodeFile.objects.filter(
        author=request.user).prefetch_related('checkcode')
    return render(request, 'files/index.html', {'files': files})
