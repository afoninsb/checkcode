from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CustomUserCreationForm


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"
