from django import  forms
from .models import User
import re
from django.utils import timezone
from datetime import date  
# import bcrypt

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
            
    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
            
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'email', 'password']
       

   
    def clean_first_name(self):
        typing = self.cleaned_data.get('first_name', '').strip()# give me the clean title or data user typing
        if len(typing) < 2:
          raise forms.ValidationError("firstName must be at least 2 characters long.")
        return typing

    def clean_last_name(self):
            typing = self.cleaned_data.get('last_name', '').strip()# give me the clean title or data user typing
            if len(typing) < 2:
                raise forms.ValidationError("lastName must be at least 2 characters long.")
            return typing
    
    def clean_email(self):
            typing = self.cleaned_data.get('email', '').strip()
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(typing):
                raise forms.ValidationError("Invalid email address!")
            if User.objects.filter(email=typing).exists():
                raise forms.ValidationError("Email already registered.")
            return typing
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # verify password constraints while it's still plain text
        if password and len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")

        # compare password field with confirm password field
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data
    


class LoginForm(forms.Form):  
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    def clean_email(self):
        typing = self.cleaned_data.get('email', '').strip()
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(typing):
            raise forms.ValidationError("Invalid email address!")
        return typing