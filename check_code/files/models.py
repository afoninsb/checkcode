from django.contrib.auth import get_user_model
from django.db import models

from users.models import CustomUser


def user_directory_path(instance, filename):
    return f'user_{instance.author.id}/{filename}'


class CheckStatus(models.TextChoices):
    """Статусы проверки."""
    ACCEPTED = 'accepted', 'Принят'
    REJECTED = 'rejected', 'Отклонён'


class FileStatus(models.TextChoices):
    """Статусы файлов."""
    NEW = 'new', 'Новый'
    UPDATED = 'updated', 'Обновлён'
    ACCEPTED = 'accepted', 'Принят'
    REJECTED = 'rejected', 'Отклонён'


class CodeFile(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
    status = models.CharField(
        'Статус файла',
        max_length=8,
        choices=FileStatus.choices,
        default=FileStatus.NEW
    )
    description = models.CharField(
        'Описание',
        max_length=256,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='files',
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
        db_index=True
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.upload.name.split('/')[-1]


class CheckCode(models.Model):
    code = models.ForeignKey(
        CodeFile,
        on_delete=models.CASCADE,
        verbose_name='Файл',
        related_name='checkcode',
    )
    time = models.DateTimeField(
        'Дата проверки',
        auto_now_add=True,
        db_index=True
    )
    result = models.TextField(
        'Отчёт о проверке',
        blank=True,
        null=True
    )
    status = models.CharField(
        'Статус проверки',
        max_length=8,
        choices=CheckStatus.choices,
    )
    sent_email = models.BooleanField('Email отправлен?', default=True)

    class Meta:
        ordering = ['-time']
        verbose_name = 'Проверка'
        verbose_name_plural = 'Проверки'
