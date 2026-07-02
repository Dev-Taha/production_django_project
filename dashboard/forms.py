import bcrypt
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User


class AccountSettingsForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Last name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Email address',
        'disabled': 'disabled'
    }))
    full_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Full name'
    }))
    academic_title = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Academic title'
    }))
    institution = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'University or institute'
    }))
    field_of_study = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Field of study'
    }))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'settings-input',
        'rows': 4,
        'placeholder': 'Short bio'
    }))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*'
    }))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'settings-input',
        'placeholder': 'New password'
    }))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'settings-input',
        'placeholder': 'Confirm password'
    }))

    def __init__(self, *args, current_user=None, **kwargs):
        self.current_user = current_user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError('Email is required.')
        if User.objects.filter(email__iexact=email).exclude(id=self.current_user.id).exists():
            raise ValidationError('Email already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = (cleaned_data.get('first_name') or '').strip()
        last_name = (cleaned_data.get('last_name') or '').strip()
        full_name = (cleaned_data.get('full_name') or '').strip()
        new_password = cleaned_data.get('new_password') or ''
        confirm_password = cleaned_data.get('confirm_password') or ''

        if not first_name and not last_name and not full_name:
            self.add_error('full_name', 'Please provide at least a full name or first/last name.')

        if new_password or confirm_password:
            if len(new_password) < 8:
                self.add_error('new_password', 'Password must be at least 8 characters long.')
            if new_password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data
