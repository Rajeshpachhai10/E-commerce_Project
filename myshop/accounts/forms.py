from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()    

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'phone' ,'street_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'

        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['street_address'].widget.attrs['placeholder'] = 'Enter your address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'


 

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # rename label and placeholder to email
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'


    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=email)
            return user.username
        except User.DoesNotExist:
            return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'dob', 'bio']
        widgets = {
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select your date of birth',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "Share a little about yourself — your interests, what you're passionate about, or anything you'd like others to know!",
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'dob': 'Date of Birth',
            'bio': 'About You',
            'profile_picture': 'Profile Picture',
        }