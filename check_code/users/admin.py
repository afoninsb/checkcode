from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser
from files.admin import CodeFileInline


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = (
        'id',
        'email',
        'is_staff',
    )
    fieldsets = [
        ('ЛОГИН', {'fields': ['email', 'password']}),
        ('ИНФО', {'fields': ['is_staff']}),
    ]
    list_filter = ('is_staff',)
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (CodeFileInline, )
