from django.contrib import admin
from files.models import CheckCode, CodeFile


class CodeFileInline(admin.TabularInline):
    model = CodeFile


class CheckInline(admin.TabularInline):
    model = CodeFile


@admin.register(CodeFile)
class CodeFileAdmin(admin.ModelAdmin):
    """Представление файлов в админке."""
    list_display = (
        'id',
        'upload',
        'status',
        'description',
        'author',
        'created_at',
        'updated_at',
        'check_result'
    )
    list_filter = ('status', 'author')
    search_fields = ('author', )
    readonly_fields = ('check_result',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('checkcode')

    def check_result(self, obj):
        """Результат провкерки"""
        if obj.checkcode.all():
            return obj.checkcode.first().result

    check_result.short_description = 'Результат последней проверки'


@admin.register(CheckCode)
class CheckCodeAdmin(admin.ModelAdmin):
    """Форма проверок в админке."""
    list_display = ('id', 'code', 'time', 'result', 'status', 'sent_email')
    list_filter = ('status', )
