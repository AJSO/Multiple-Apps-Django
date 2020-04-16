from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile, ProfilePic
from django.forms import ValidationError

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ProfileForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'address',
            'city',
            'country',
            'postal_code',
            'about',     
        ]

class AvatarForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = [
            'image',
        ]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label = "Username")
    password = forms.CharField(max_length=100, label = 'Password', widget = forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Invalid Email or Password, Check and try again.!')
            
        return super(LoginForm, self).clean()

