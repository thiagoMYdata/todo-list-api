from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User