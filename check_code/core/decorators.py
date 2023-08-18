from django.http import HttpResponseForbidden
from files.models import CodeFile


def is_author(func):
    """Проверка, что пользователь - автор файла."""
    def wrapper(request, **kwargs):
        file_id = kwargs.get('file_id')
        if not file_id:
            return func(request, **kwargs)
        try:
            code = CodeFile.objects.get(pk=file_id, author=request.user)
        except CodeFile.DoesNotExist:
            return HttpResponseForbidden()
        else:
            kwargs['code'] = code
            return func(request, **kwargs)
    return wrapper
