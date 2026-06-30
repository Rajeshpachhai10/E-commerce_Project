from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import get_user_model
# from .models import CustomUser

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
    