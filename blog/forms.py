from django import forms
# from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('post', 'name', 'email', 'body')

    def _clean_fields(self):
        self.fields.pop('post_id')
        super()._clean_fields()

