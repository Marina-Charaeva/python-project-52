from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomAuthenticationForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': _('Username'),
            'class': 'form-control',
            'autofocus': True
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': _('Password'),
            'class': 'form-control'
        })

class CustomUserCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': _('Username'),
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': _('Password'),
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': _('Password confirmation'),
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': _('First name'),
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': _('Last name'),
            'class': 'form-control'
        })
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']