from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from wibu_catalog.models import Comments


class LoginForm(AuthenticationForm):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            }
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        ),
        label="Password",
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]


class ChangePasswordForm(AuthenticationForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Current Password')
            }
        ),
        label=_('Current Password')
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('New Password')
            }
        ),
        label=_('New Password')
    )
    new_password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm New Password')
            }
        ),
        label=_('New Password Confirmation')
    )


class UserRegistrationForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Name')
            }
        ),
        label=_('Name')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email Address')
            }
        ),
        label=_('Email Address')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password')
            }
        ),
        label=_('Password')
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm Password')
            }
        ),
        label=_('Confirm Password')
    )
    dateOfBirth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Date of Birth'),
                'type': 'date'
            }
        ),
        label=_('Date of Birth'),
        required=False
    )
