from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    # The variables must be 'username' and 'password' or it will not work
    username    = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": 'form-control', 'style': 'width:250px'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'style': 'width:250px'}))

    class Meta:
        model   = User
        fields  = ('email', 'password')

class RegisterForm(forms.Form):
    username    = forms.EmailField()
    full_name   = forms.CharField()
    password    = forms.CharField(widget=forms.PasswordInput)
    password2   = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    
    def clean_email(self):
        username = self.cleaned_data.get("username")
        return username

    def clean_name(self):
        full_name = self.cleaned_data.get("full_name")
        return full_name

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        return password2
    
    def clean(self):
        data = self.cleaned_data
        return data