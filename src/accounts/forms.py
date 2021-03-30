from django import forms
from django.contrib.auth import get_user_model

from django.forms import ModelForm

User = get_user_model()

class LoginForm(forms.Form):
    # The variables must be 'username' and 'password' or it will not work
    username    = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": 'form-control', 'style': 'width:250px'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'style': 'width:250px'}))

    class Meta:
        model   = User
        fields  = ('email', 'password')

class RegisterForm(forms.Form):
    username    = forms.EmailField(widget=forms.EmailInput(attrs={'id':'username', 'name':'username'}), required=True)
    full_name   = forms.CharField(widget=forms.TextInput(attrs={'id':'full_name', 'name':'full_name'}), required=True)
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password', 'name':'password'}), required=True)
    password2   = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'id':'password2', 'name':'password2'}), required=True)
    
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
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # if password != password2:
        #     raise forms.ValidationError("Passwords must match")
        return data

class UserUpdateForm(ModelForm):
    email = forms.EmailField()
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control account_field px-0 py-1',"id": "full_name_box", "name": "full_name"}))
    old_password = forms.CharField()
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'full_name',
            'profile_pic',
            'genres',
        )
    
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return data

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user