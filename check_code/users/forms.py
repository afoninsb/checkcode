from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email',)
